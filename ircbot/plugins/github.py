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
        self.prefix = "{}[GitHub]{}".format(Format.GREEN, Format.RESET)
        self.bot = self.application._ctx

    @coroutine
    def post(self):
        hook_type = self.request.headers['X-GitHub-Event']
        body_text = self.request.body.decode()
        body = json.loads(body_text)

        target_channel = self.get_argument("channel", None, None)

        # logger.debug("Github Hook Type: {}".format(hook_type))
        # logger.debug("Body: {}".format(body_text))

        method_name = "handle_{}".format(hook_type.lower().replace(" ", "_"))

        try:
            handler = getattr(self, method_name)
        except AttributeError:
            pass
        else:
            yield handler(target_channel, body)

    @coroutine
    def handle_ping(self, target_channel, body):
        logger.debug("GitHub PING <==> PONG")
        self.bot.message("#" + target_channel, "{} PING".format(self.prefix))   

    @coroutine
    def handle_push(self, target_channel, body):
        who = body['head_commit']['committer']['name']
        repo = body['repository']['full_name']
        commits = body['commits']
        commit_suffix = "s" if len(commits) > 1 else ""
        self.bot.message("#" + target_channel, "{} {}{}{} has pushed {}{:d}{} commit{} to {}{}{}".format(
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

        self.bot.message("#" + target_channel, "{} {}{}{} - {}{}{}".format(
            self.prefix,
            Format.BLUE, repo, Format.RESET,
            colour[body['state']], what_happened, Format.RESET
        ))

    @coroutine
    def handle_pull_request(self, target_channel, body):
        repo = body['repository']['full_name']
        pr_info = "Pull Request {}#{:d}: {}{}".format(Format.GREEN, body['pull_request']['number'], body['pull_request']['title'], Format.RESET)
        action = body['action']
        if action == "closed" and body['pull_request']['merged']:
            state = "merged"
        else:
            state = action

        if state == "assigned":
            message = "{} {}{}{} - {}{}{} assigned {} to {}{}{}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info,
                Format.BLUE, body['pull_request']['assignee']['login'], Format.RESET
            )
        elif state == "unassigned":
            message = "{} {}{}{} - {}{}{} unassigned {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "labeled":
            message = "{} {}{}{} - {}{}{} added label {}{}{} to {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                pr_info
            )
        elif state == "unlabeled":
            message = "{} {}{}{} - {}{}{} removed label {}{}{} from {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                pr_info
            )
        elif state == "opened":
            message = "{} {}{}{} - {}{}{} opened {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "closed":
            message = "{} {}{}{} - {}{}{} closed {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "reopened":
            message = "{} {}{}{} - {}{}{} re-opened {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "synchronize":
            message = "{} {}{}{} - {}{}{} pushed new commits to {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )
        elif state == "merged":
            message = "{} {}{}{} - {}{}{} merged {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                pr_info
            )

        self.bot.message("#" + target_channel, message)

    @coroutine
    def handle_issues(self, target_channel, body):
        repo = body['repository']['full_name']
        info = "issue {}#{:d}: {}{}".format(Format.GREEN, body['issue']['number'], body['issue']['title'], Format.RESET)
        state = body['action']

        if state == "assigned":
            message = "{} {}{}{} - {}{}{} assigned {} to {}{}{}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info,
                Format.BLUE, body['issue']['assignee']['login'], Format.RESET
            )
        elif state == "unassigned":
            message = "{} {}{}{} - {}{}{} unassigned {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "labeled":
            message = "{} {}{}{} - {}{}{} added label {}{}{} to {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                info
            )
        elif state == "unlabeled":
            message = "{} {}{}{} - {}{}{} removed label {}{}{} from {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                Format.GREY, body['label']['name'], Format.RESET,
                info
            )
        elif state == "opened":
            message = "{} {}{}{} - {}{}{} opened {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "closed":
            message = "{} {}{}{} - {}{}{} closed {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )
        elif state == "reopened":
            message = "{} {}{}{} - {}{}{} re-opened {}".format(
                self.prefix,
                Format.ORANGE, repo, Format.RESET,
                Format.BLUE, body['sender']['login'], Format.RESET,
                info
            )

        self.bot.message("#" + target_channel, message)

    @coroutine
    def handle_issue_comment(self, target_channel, body):
        repo = body['repository']['full_name']
        info = "{}#{:d}: {}{}".format(Format.GREEN, body['issue']['number'], body['issue']['title'], Format.RESET)

        message = "{} {}{}{} - {}{}{} commented on {}".format(
            self.prefix, Format.ORANGE, repo, Format.RESET,
            Format.BLUE, body['sender']['login'], Format.RESET,
            info
        )

        self.bot.message("#" + target_channel, message)
