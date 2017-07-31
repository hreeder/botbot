import requests

from ircbot import bot


@bot.command('cat')
def cat_command(bot, channel, sender, args):
    uri = "http://random.cat/meow"
    data = requests.get(uri).json()
    bot.message(channel, "{}".format(data['file']))
