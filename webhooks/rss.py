import logging
import json

from tornado.gen import coroutine
from tornado.web import RequestHandler
from util import Format

logger = logging.getLogger(__name__)


class RSSHandler(RequestHandler):
    def initialize(self):
        self.prefix = "%s[RSS]%s" % (Format.GREEN, Format.RESET)
        self.bot = self.application._ctx

    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode())
        target_channel = self.get_argument("channel", None, None)

        data['prefix'] = self.prefix
        self.bot.message(target_channel, "{prefix} {title} - {description} - {link}".format(**data))
