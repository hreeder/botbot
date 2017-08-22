import requests

from ircbot import bot


@bot.command('dog')
def dog_command(bot, channel, sender, args):
    uri = "https://random.dog/woof.json"
    data = requests.get(uri).json()
    bot.message(channel, "{}".format(data['url']))
