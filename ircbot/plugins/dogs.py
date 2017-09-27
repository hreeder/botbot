import requests

from ircbot import bot


@bot.command(['dog', 'dogs'])
def dog_command(bot, channel, sender, args=1):
    """Get dog gifs! {bot.trigger}dog[s] [number of dog gifs]"""
    uri = "https://random.dog/woof.json"
    data = [requests.get(uri).json()['url'] for _ in range(args)]
    bot.message(channel, " - ".join(data))
