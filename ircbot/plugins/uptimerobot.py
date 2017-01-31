import logging
import json

from tornado.gen import coroutine
from tornado.web import RequestHandler
from ircbot import bot, Format

logger = logging.getLogger(__name__)


@bot.webhook("/uptimerobot")
class UptimeRobotHandler(RequestHandler):
    def initialize(self):
        self.prefix = "{}[UptimeRobot]{}".format(Format.GREEN, Format.RESET)
        self.bot = self.application._ctx

    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode())
        target_channel = data['channel']

        monitorFriendlyName = self.get_argument('monitorFriendlyName', None, True)
        alertTypeFriendlyName = self.get_argument('alertTypeFriendlyName', None, True)
        alertDetails = self.get_argument('alertDetails', None, True)

        self.bot.message(
            target_channel,
            "{prefix} {monitor} is now {alert} - {details}".format(
                prefix=self.prefix,
                monitor=monitorFriendlyName,
                alert=alertTypeFriendlyName,
                details=alertDetails
            )
        )
