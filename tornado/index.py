import tornado.ioloop, tornado.web, os
from tornado.log import enable_pretty_logging
from tornado import websocket
enable_pretty_logging()

class fuckWebSockets(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True
	def open(self):
		print 'Websocket opened'
	def on_message(self, message):
		print message
		self.write_message(u'You said ' + message)
	def on_close(self):
		print 'Websocket closed'

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print 'hi main'
		self.render("templates/index.html")

def make_app():
	handlers = [(r"/", MainHandler), (r"/websocket", fuckWebSockets)]
	settings = {
			"static_path": "static"
	}
	return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
	app = make_app()
	#app.listen(8181)
	print 'before the action'
	app.listen(443, ssl_options={
		"certfile": "map.crt",
		"keyfile": "map.key", 
	})
	print 'after listening'
	tornado.ioloop.IOLoop.current().start()
