import requests


def bunny_command(bot, channel, sender, args):
    uri = "https://api.bunnies.io/v2/loop/%s/?media=gif"
    part = "random"
    if args:
        try:
            part = str(int(args[0]))
        except ValueError:
            pass
    data = requests.get(uri % part)
    bot.message(channel, data.json()['media']['gif'])
