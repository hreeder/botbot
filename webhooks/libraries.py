import logging
import json

from tornado.gen import coroutine
from tornado.web import RequestHandler
from util import Format

logger = logging.getLogger(__name__)


class LibrariesHandler(RequestHandler):
    def initialize(self):
        self.prefix = "%s[LibrariesIO]%s" % (Format.GREEN, Format.RESET)
        self.bot = self.application._ctx

    @coroutine
    def post(self):
        logger.debug("TEST")
        data = json.loads(self.request.body.decode())
        target_channel = self.get_argument("channel", None, None)

        event = data['event']
        method_name = "handle_%s" % (event.lower())

        try:
            handler = getattr(self, method_name)
        except AttributeError:
            pass
        else:
            yield handler(target_channel, data)

    @coroutine
    def handle_new_version(self, target_channel, data):
        self.bot.message(target_channel, "%s %s%s%s - A library has been updated: %s%s%s - %sv%s%s (%s%s%s)" % (
            self.prefix,
            Format.BLUE, data['repository'], Format.RESET,
            Format.AQUA, data['name'], Format.RESET,
            Format.ORANGE, data['version'], Format.RESET,
            Format.GREEN, data['platform'], Format.RESET
        ))
