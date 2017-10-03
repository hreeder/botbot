import requests

from ircbot import bot


@bot.command('bunny')
def bunny_command(bot, channel, sender, args):
<<<<<<< HEAD
    uri = "https://api.bunnies.io/v2/loop/{}/?media=gif"
=======
    """Usage: {bot.trigger}bunny [bunny id] - Grabs a bunny gif, if an id isn't specifed one will be chosen"""
    uri = "https://api.bunnies.io/v2/loop/%s/?media=gif"
>>>>>>> bb1bbd37bb51e6f76bc3405e5b31138b887faf0f
    part = "random"
    if args:
        try:
            part = str(int(args[0]))
        except ValueError:
            pass
    data = requests.get(uri.format(part)).json()
    bot.message(channel, "https://bunnies.io/#{} - {}".format(data['id'], data['media']['gif']))


@bot.command('bunnybomb')
def bunny_bomb(bot, channel, sender, args):
    """ Usage: {bot.trigger}bunnybomb [N] - Sends N bunnies to the current channel. N defaults to 5. Nmax = 10 """
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
