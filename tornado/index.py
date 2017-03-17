import tornado.ioloop, tornado.web, os, json, sys
from tornado.log import enable_pretty_logging
from tornado import websocket
import numpy as np

sys.path.append('../src')
from gmm import test_sample_gmms
from features import compute_features
import utilities

class audioSocket(websocket.WebSocketHandler):    
    audio = []
    def check_origin(self, origin):
        return True

    def open(self):
        print 'websocket opened'

    def on_message(self, message):
        if message:
            message = utilities.convert(json.loads(message))
            if message['type'] == 'recording':
                self.record_audio(message)

    def on_close(self):
        print 'websocket closed'

    def record_audio(self, message):
        if message['text'] == 'chunk':
            data = [message['data'][str(x)] for x in range(len(message['data']))]
            self.audio += data
        elif message['text'] == 'done':
            self.write_message('ayyyy recording finished')
            self.write_message(self.classify(self.audio))
            self.audio = []

    def classify(self, signal):
        gmm_dict = utilities.load('../professor_gmms.p')

        mfccs = compute_features(np.array(signal), features=[mfcc])
        pred, probs = test_sample_gmms(gmm_dict, mfccs['features'])

        print probs
        return pred

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

def make_app():
    handlers = [(r"/", MainHandler), (r"/websocket", audioSocket)]
    settings = {
            "static_path": "static"
    }
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    enable_pretty_logging()
    audio = []    

    app = make_app()

    app.listen(443,
        ssl_options={
            "certfile": "map.crt",
            "keyfile": "map.key", })

    tornado.ioloop.IOLoop.current().start()
