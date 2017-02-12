import requests

from ircbot import bot


@bot.command('bunny')
def bunny_command(bot, channel, sender, args):
    uri = "https://api.bunnies.io/v2/loop/%s/?media=gif"
    part = "random"
    if args:
        try:
            part = str(int(args[0]))
        except ValueError:
            pass
    data = requests.get(uri % part).json()
    bot.message(channel, "https://bunnies.io/#%s - %s" % (data['id'], data['media']['gif']))


@bot.command('bunnybomb')
def bunny_bomb(bot, channel, sender, args):
    """ Usage: $bunnybomb [N] - Sends N bunnies to the current channel. N defaults to 5. Nmax = 10 """
    n = 5
    if args:
        try:
            n = int(args[0])
        except ValueError:
            pass
    if n > 10:
        n = 10
    for _ in range(n):
        bunny_command(bot, channel, sender, None)
