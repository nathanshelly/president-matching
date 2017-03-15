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
def handle_requests(ws):
    while ws.connected:
        msg = ws.receive()
        if msg:
            msg = utilities.convert(json.loads(msg))
            if msg['type'] == 'recording':
                record_audio(ws)


def record_audio(ws, ):
    audio = []
    recording_msg = msg
    print 'ayy recording started'
    while recording_msg['type'] == 'recording':
        print msg['text']
        data = [msg['data'][str(x)] for x in range(len(msg['data']))]
        audio += data

        recording_msg = ws.receive()
        while not recording_msg:
            recording_msg = ws.receive()

        recording_msg = utilities.convert(json.loads(recording_msg))

    print 'ayy recording finished'
    ws.send('hey')
    # ws.send(classify(audio))

@app.route("/")
def index():
    return render_template('index.html')

def classify(signal, classifier_type = 'gmm'):
    gmm_dict = utilities.load('../src/nathan_sasha_pardo_gmm_dict.p')
    mfccs = mfcc_features(signal)
    return test_sample_gmms(gmm_dict, mfccs)

def streaming_classify(signal, current_probabilities, classifiers_path = 'nathan_sasha_pardo_gmm_dict.p', classifier_type = 'gmm'):
    # signal is buffer of 4096 data points
    signal = streaming_mfcc_features(signal)
    probabilities = streaming_test_sample_gmms(utilities.load(classifiers_path), signal)
    
    # if not current_probabilities:
    #     current_probabilities = {label: 0 for label in probabilities.keys()}
    # updated_dictionary = {key: current_probabilities.get(key, 0) + probabilities.get(key, 0) for key in set(current_probabilities) & set(probabilities)}
    
    # .get should handle empty current_probabilities
    updated_probabilites = {key: probabilities.get(key, 0) + current_probabilities.get(key, 0) for key in probabilities}
    return updated_probabilites
    
if __name__ == "__main__":
    app.run(debug = True)