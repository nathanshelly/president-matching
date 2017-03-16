from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import json, sys
import numpy as np

sys.path.append('../src')
# from gmm import streaming_test_sample_gmms, test_sample_gmms
# from knn import test_knn
# from mfcc import streaming_mfcc_features, mfcc_feature

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
                record_audio(ws, msg)

def record_audio(ws, msg):
    audio = []
    recording_msg = msg
    while recording_msg['type'] == 'recording':
        data = [recording_msg['data'][str(x)] for x in range(len(recording_msg['data']))]
        audio += data

        recording_msg = ws.receive()
        while not recording_msg:
            recording_msg = ws.receive()

        recording_msg = utilities.convert(json.loads(recording_msg))
    
    print audio
    # let s = Math.max(-1, Math.min(1, input[i]));
    # output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        
    # ws.send(classify(audio))
    ws.send('hi')

@app.route("/")
def index():
    return render_template('index.html')

def classify(signal, classifier_type = 'gmm'):
    mfccs = mfcc_feature(signal)
    
    if classifier_type == 'knn':
        pass
        # classification = test_knn()
    else:
        gmm_dict = utilities.load('../nathan_sasha_pardo_gmm_dict.p')
        classification = test_sample_gmms(gmm_dict, mfccs)
    
    return 

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