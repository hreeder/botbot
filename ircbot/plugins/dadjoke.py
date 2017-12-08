import requests

from ircbot import bot


@bot.command('dadjoke')
def dad_joke(bot, channel, sender, args):
    """Return a random dad - Usage: {bot.trigger}dadjoke"""
    endpoint = "https://icanhazdadjoke.com/"
    data = requests.get(endpoint, headers={"Accept": "application/json"}).json()

    response = data['joke']

    bot.message(channel, "{}: {}".format(sender, response))
