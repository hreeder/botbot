import logging

from tornado.httpserver import HTTPServer
from tornado.web import Application

logger = logging.getLogger(__name__)


def setup_webserver(bot):
    logger.debug("Setting up webserver")
    app = Application()
    app._ctx = bot

    server = HTTPServer(app, io_loop=bot.event_loop.io_loop)

    return app, server
