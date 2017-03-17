from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import json, sys
import numpy as np

sys.path.append('../src')
from gmm import streaming_test_sample_gmms, test_sample_gmms
from knn import test_knn
from features import compute_features
from mfcc import mfcc, filtered_mfcc
from data import normalize
import utilities

app = Flask(__name__)
ws = GeventWebSocket(app)

@ws.route("/websocket")
def handle_requests(ws):
    print ws.timeout
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
        ws.send('None')
        data = [recording_msg['data'][str(x)] for x in range(len(recording_msg['data']))]
        audio += data

        recording_msg = ws.receive()
        while not recording_msg:
            ws.send('None')
            recording_msg = ws.receive()

        recording_msg = utilities.convert(json.loads(recording_msg))
    
    ws.send('ayyyy recording finished')
    # ws.send(classify(audio))

@app.route("/")
def index():
    return render_template('index.html')

def classify(signal):
    signal = normalize(signal)
    gmm_dict = utilities.load('../professor_gmms.p')

    mfccs = compute_features(np.array(signal), features=[mfcc])
    
    pred, probs = test_sample_gmms(gmm_dict, mfccs['features'])
    
    print probs
    return pred
    
if __name__ == "__main__":
    app.run(debug = True)
