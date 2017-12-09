import logging

from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler

logger = logging.getLogger(__name__)


def setup_webserver(bot):
    logger.debug("Setting up webserver")
    app = Application()
    app._ctx = bot

    server = HTTPServer(app, io_loop=bot.event_loop.io_loop)

    return app, server


class BaseRequestHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
