'''
    Github Botbot Webhook Support
    Implementation influenced by https://bitbucket.org/KitB/pircel-bitbucket-notifier
'''
import logging
import json

from tornado.gen import coroutine
from tornado.web import RequestHandler
from util import Format

logger = logging.getLogger(__name__)


class GithubHandler(RequestHandler):
    def initialize(self):
        self.prefix = "%s[Github]%s" % (Format.GREEN, Format.RESET)
        self.bot = self.application._ctx

    @coroutine
    def post(self):
        hook_type = self.request.headers['X-GitHub-Event']
        body = json.loads(self.request.body.decode())

        target_channel = self.get_argument("channel", None, None)

        logger.debug("Github Hook Type: %s" % hook_type)
        logger.debug("Body: %s" % json.dumps(body))

        method_name = "handle_%s" % (hook_type.lower().replace(" ", "_"))

        try:
            handler = getattr(self, method_name)
        except AttributeError:
            pass
        else:
            yield handler(target_channel, body)

    @coroutine
    def handle_ping(self, target_channel, body):
        logger.debug("Github PING <==> PONG")
