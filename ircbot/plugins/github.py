'''
    Github Botbot Webhook Support
    Implementation influenced by https://bitbucket.org/KitB/pircel-bitbucket-notifier
'''
import logging
import json

from tornado.gen import coroutine
from tornado.web import RequestHandler
from ircbot import bot, Format

logger = logging.getLogger(__name__)


@bot.webhook("/github")
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

        # logger.debug("Github Hook Type: %s" % hook_type)
        # logger.debug("Body: %s" % body_text)

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
            Format.TEAL, len(commits), Format.RESET,
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
            "pending": Format.TEAL
        }

        self.bot.message("#" + target_channel, "%s %s%s%s - %s%s%s" % (
            self.prefix,
            Format.BLUE, repo, Format.RESET,
            colour[body['state']], what_happened, Format.RESET
        ))

    @coroutine
    def handle_pull_request(self, target_channel, body):
        repo = body['repository']['full_name']
        pr_info = "Pull Request %s#%d: %s%s" % (Format.GREEN, body['pull_request']['number'], body['pull_request']['title'], Format.RESET)
        action = body['action']
        if action == "closed" and body['pull_request']['merged']:
            state = "merged"
        else:
            state = action

        if state == "assigned":
            message = "%s %s%s%s - %s%s%s assigned %s to %s%s%s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info,
                Format.BLUE, body['pull_request']['assignee']['login'], Format.RESET
            )
        elif state == "unassigned":
            message = "%s %s%s%s - %s%s%s unassigned %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "labeled":
            message = "%s %s%s%s - %s%s%s added label %s%s%s to %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                pr_info
            )
        elif state == "unlabeled":
            message = "%s %s%s%s - %s%s%s removed label %s%s%s from %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                pr_info
            )
        elif state == "opened":
            message = "%s %s%s%s - %s%s%s opened %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "closed":
            message = "%s %s%s%s - %s%s%s closed %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "reopened":
            message = "%s %s%s%s - %s%s%s re-opened %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "synchronize":
            message = "%s %s%s%s - %s%s%s pushed new commits to %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "merged":
            message = "%s %s%s%s - %s%s%s merged %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )

        self.bot.message("#" + target_channel, message)

    @coroutine
    def handle_issues(self, target_channel, body):
        repo = body['repository']['full_name']
        info = "issue %s#%d: %s%s" % (Format.GREEN, body['issue']['number'], body['issue']['title'], Format.RESET)
        state = body['action']

        if state == "assigned":
            message = "%s %s%s%s - %s%s%s assigned %s to %s%s%s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info,
                Format.BLUE, body['issue']['assignee']['login'], Format.RESET
            )
        elif state == "unassigned":
            message = "%s %s%s%s - %s%s%s unassigned %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "labeled":
            message = "%s %s%s%s - %s%s%s added label %s%s%s to %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                info
            )
        elif state == "unlabeled":
            message = "%s %s%s%s - %s%s%s removed label %s%s%s from %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                info
            )
        elif state == "opened":
            message = "%s %s%s%s - %s%s%s opened %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "closed":
            message = "%s %s%s%s - %s%s%s closed %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "reopened":
            message = "%s %s%s%s - %s%s%s re-opened %s" % (
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )

        self.bot.message("#" + target_channel, message)

    @coroutine
    def handle_issue_comment(self, target_channel, body):
        repo = body['repository']['full_name']
        info = "%s#%d: %s%s" % (Format.GREEN, body['issue']['number'], body['issue']['title'], Format.RESET)

        message = "%s %s%s%s - %s%s%s commented on %s" % (
            self.prefix, Format.ORANGE, repo, Format.RESET,
            Format.BLUE, body['sender']['login'], Format.RESET,
            info
        )

        self.bot.message("#" + target_channel, message)
