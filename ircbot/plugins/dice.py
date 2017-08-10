import random
import re

from ircbot import bot


@bot.command('roll')
def roll(bot, channel, sender, args):
    """ Roll some dice """
    n = 1
    sides = 6
    if args and re.match(r"^(?P<num>[0-9]+)d(?P<sides>[0-9]+)$", args[0]):
        m = re.search(r"^(?P<num>[0-9]+)d(?P<sides>[0-9]+)$", args[0])
        n = int(m.group('num')) if int(m.group('num')) < 20 else 1
        sides = int(m.group('sides')) if int(m.group('sides')) > 0 else 6

    results = [str(random.randint(1, sides)) for _ in range(n)]

    bot.message(channel, "Rolls ({}d{}): {}".format(n, sides, ", ".join(results)))
