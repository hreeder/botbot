import requests

from ircbot import bot


@bot.command(['dog', 'doggo'])
def dog_command(bot, channel, sender, args):
    """Get a dog gif! {bot.trigger}dog[go]"""
    uri = "https://random.dog/woof.json"
    data = requests.get(uri).json()['url']
    bot.message(channel, "{}".format(data))

@bot.command(['dogs', 'dogbomb'])
def dog_bomb(bot, channel, sender, args):
    """Usage: {bot.trigger}(dogs|dogbomb) [N] - Sends N dogs to the current channel. N defaults to 3. N max = 10."""
    n = 3
    if args:
        try:
            n = int(args[0])
        except ValueError:
            pass
    if n > 10:
        n = 10
    for _ in range(n):
        dog_command(bot, channel, sender, None)
