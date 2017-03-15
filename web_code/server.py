from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import json, collections

app = Flask(__name__)
ws = GeventWebSocket(app)

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

@ws.route("/websocket")
def audio(ws):
    while ws.connected:
        msg = ws.receive()
        if msg:
            msg = convert(json.loads(msg))
            print msg
            if msg['type'] == 'testing':
                print [x*x for x in msg['data']]
                print msg['text']

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)