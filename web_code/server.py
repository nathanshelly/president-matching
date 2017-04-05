import tornado.ioloop, tornado.web, os, json, sys
from tornado.log import enable_pretty_logging
from tornado import websocket
import numpy as np

sys.path.append('../src')
from gmm import test_signal_against_gmms
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
            self.write_message(json.dumps(self.classify(self.audio)))
            self.audio = []

    def classify(self, signal):
        gmm_dict = utilities.load('../pickles/professor_gmms_train.p')

        mfccs = compute_features(np.array(signal))
        pred, probs = test_signal_against_gmms(gmm_dict, mfccs['features'])

        print probs
        return {'type': 'result', 'pred': pred, 'probs': probs}

def make_app():
    handlers = [(r"/websocket", audioSocket)]
    return tornado.web.Application(handlers)

if __name__ == "__main__":
    enable_pretty_logging()
    app = make_app()
    app.listen(8000, address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
