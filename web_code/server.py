from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import json

app = Flask(__name__)
ws = GeventWebSocket(app)

@ws.route("/websocket")
def audio(ws):
    while ws.connected:
        msg = ws.receive()
        if msg:
            msg = utilities.convert(json.loads(msg))
            # print msg
            print msg['type']
            if msg['type'] == 'recording':
                print msg['text']
                data = [msg['data'][str(x)] for x in range(len(msg['data']))]
                utilities.save(data, 'temp.p')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)