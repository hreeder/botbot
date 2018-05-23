import random
import re

from ircbot import bot

THANKS_REGEX = re.compile(r"^thank(s| you),? {}$".format(bot.config['IRC']['nick']), re.IGNORECASE)
FUCK_REGEX = re.compile(r"^fuck you,? {}$".format(bot.config['IRC']['nick']), re.IGNORECASE)

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
    if THANKS_REGEX.match(message.strip()):
        bbot.message(channel, random.choice(THANKS_REPLIES).format(sender))
    elif FUCK_REGEX.match(message.strip()):
        bbot.message(channel, random.choice(FUCK_REPLIES).format(sender))
