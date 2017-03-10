from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return "fuck"

@app.route("/hello")
def hello():
	return "Hello there"

@app.route("/testing")
def testing(name=None):
	# return "hi"
	return render_template('testing.html', name=name)

if __name__ == "__main__":
	app.run()