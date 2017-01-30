import logging

from .bot import BotBot
from .formatting import Format

logger = logging.getLogger(__name__)

logger.debug("Creating BotBot")
bot = BotBot()
logger.debug("BotBot Created")
