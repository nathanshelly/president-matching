from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import json, sys

sys.path.append('../src')
# from gmm import streaming_test_sample_gmms, test_sample_gmms
# from mfcc import streaming_mfcc_features, mfcc_features
import utilities

app = Flask(__name__)
ws = GeventWebSocket(app)

@ws.route("/websocket")
def audio(ws):
    while ws.connected:
        msg = ws.receive()
        if msg:
            msg = utilities.convert(json.loads(msg))
            if msg['type'] == 'recording':
                audio = []
                recording_msg = msg
                print 'ayy recording started'
                while recording_msg['type'] == 'recording':
                    print msg['text']
                    data = [msg['data'][str(x)] for x in range(len(msg['data']))]
                    audio += data
                    
                    recording_msg = ws.receive()
                    # print recording_msg

                    while not recording_msg:
                        recording_msg = ws.receive()

                    # print recording_msg
                    recording_msg = utilities.convert(json.loads(recording_msg))
                
                print 'ayy recording finished'
                ws.send(classify(audio))

@app.route("/")
def index():
    return render_template('index.html')

def classify(signal, classifier_type = 'gmm'):
    gmm_dict = utilities.load('../src/nathan_sasha_pardo_gmm_dict.p')
    mfccs = mfcc_features(signal)
    return test_sample_gmms(gmm_dict, mfccs)


def streaming_classify(signal, current_probabilities, classifier_type = 'gmm'):
    pass
    # signal is buffer of 4096 data points
    # if not current_probabilities:
    #     current_probabilities

    # signal = streaming_mfcc_features(signal)

    # updated_dictionary = {key: x.get(key, 0) + y.get(key, 0) for key in set(x) & set(y)}



if __name__ == "__main__":
    app.run(debug = True)