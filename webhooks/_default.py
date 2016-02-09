from tornado.web import RequestHandler


class DefaultHandler(RequestHandler):
    def get(self):
        self.write("Online")
