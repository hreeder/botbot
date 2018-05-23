import random
import re

from ircbot import bot

THANKS_REGEX = re.compile(r"thank(s| you),? {}".format(bot.config['IRC']['nick']), re.IGNORECASE)
FUCK_REGEX = re.compile(r"fuck you,? {}".format(bot.config['IRC']['nick']), re.IGNORECASE)

THANKS_REPLIES = [
    'No worries, {}!',
    'I\'ve got you, {}!',
    'You\'re welcome',
    'Ain\'t no thang',
    '👉😎👉'
]

FUCK_REPLIES = [
    ':(',
    'Fair one',
    '😭',
    'Fuck you too, {}!'
]


@bot.hook()
def message_hook(bbot, channel, sender, message):
    """For when you want to say something to botbot!"""
    if re.match(THANKS_REGEX, message):
        bbot.message(channel, random.choice(THANKS_REPLIES).format(sender))
    elif re.match(FUCK_REGEX, message):
        bbot.message(channel, random.choice(FUCK_REPLIES).format(sender))
