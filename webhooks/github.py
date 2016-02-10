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
        body_text = self.request.body.decode()
        body = json.loads(body_text)

        target_channel = self.get_argument("channel", None, None)

        logger.debug("Github Hook Type: %s" % hook_type)
        logger.debug("Body: %s" % body_text)

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
        self.bot.message("#" + target_channel, "%s PING" % self.prefix)

    @coroutine
    def handle_push(self, target_channel, body):
        who = body['head_commit']['committer']['name']
        repo = body['repository']['full_name']
        commits = body['commits']
        commit_suffix = "s" if len(commits) > 1 else ""
        self.bot.message("#" + target_channel, "%s %s%s%s has pushed %s%d%s commit%s to %s%s%s" % (
            self.prefix,
            Format.BLUE, who, Format.RESET,
            Format.YELLOW, len(commits), Format.RESET,
            commit_suffix,
            Format.GREEN, repo, Format.RESET
        ))

    @coroutine
    def handle_status(self, target_channel, body):
        repo = body['repository']['full_name']
        what_happened = body['description']

        colour = {
            "success": Format.GREEN,
            "failure": Format.RED,
            "error": Format.RED,
            "pending": Format.YELLOW
        }

        self.bot.message("#" + target_channel, "%s %s%s%s - %s%s%s" % (
            self.prefix,
            Format.BLUE, repo, Format.RESET,
            colour[body['state']], what_happened, Format.RESET
        ))
