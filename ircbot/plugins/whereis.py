import datetime
import requests

from ircbot import bot


@bot.command('whereis')
def whereis(bot, channel, sender, args):
    """Where Is - Locates someone"""
    who = args[0].lower()
    targets = {
        'rikki': whereis_rikki,
        'r2zer0': whereis_rikki,
        'rhiaro': whereis_amy,
        'amy': whereis_amy,
        # 'tbrb': whereis_tbrb,
        # 'harry': whereis_tbrb,
        'alistair': whereis_alistair,
        'cazagen': whereis_cazagen
    }
    if who in targets.keys():
        targets[who](bot, channel, sender, args)
    elif who == bot.nickname.lower():
        bot.message(channel, "I am in the following places: " + ", ".join(bot.channels.keys()))
    else:
        bot.message(channel, "I do not know this '{}'. If they've got an open API reporting "
                             "their location data, I'd love to know about it though!".format(who))


def whereis_rikki(bot, channel, sender, args):
    endpoint = "http://rtrack.r2zer0.net/"
    mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
    data = requests.get(endpoint).json()
    last_updated = datetime.datetime.fromtimestamp(
        int(data['timestamp']) / 1000)
    reported = last_updated.strftime('%Y/%m/%d %H:%M')

    response = "Rikki's last location, reported on {}, was {}{}+{}".format(reported,
                                                                           mapurl,
                                                                           data['latitude'],
                                                                           data['longitude'])

    bot.message(channel, response)


# def whereis_tbrb(bot, channel, sender, args):
#     endpoint = "http://track-api.harryreeder.co.uk/ehpeeye"
#     mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
#     data = requests.get(endpoint).json()
#     response = "tbrb's last location was {}{}+{}".format(mapurl,
#                                                          data['loc']['latitude'], data['loc']['longitude'])
#     bot.message(channel, response)


def whereis_amy(bot, channel, sender, args):
    endpoint = "http://rhiaro.co.uk/where"
    data = requests.get(endpoint).json()
    bot.message(channel, data['as:summary'] + " - https://rhiaro.co.uk/arrives")


def whereis_alistair(bot, channel, sender, args):
    endpoint = "https://v2.pw/loc.json"
    mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
    data = requests.get(endpoint).json()
    last_updated = datetime.datetime.fromtimestamp(int(data['update']))
    reported = last_updated.strftime('%Y/%m/%d %H:%M')

    response = "Alistair's last location, reported on {}, was {}{}+{}".format(reported, mapurl, data['lat'], data['lon'])
    bot.message(channel, response)


def whereis_cazagen(bot, channel, sender, args):
    endpoint = "http://loc.cazagen.me/loc.json"
    mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
    data = requests.get(endpoint).json()
    last_updated = datetime.datetime.fromtimestamp(int(data['update']))
    reported = last_updated.strftime('%Y/%m/%d %H:%M')

    response = "Cameron's last location, reported on {}, was {}{}+{}".format(reported, mapurl, data['lat'], data['lon'])
    bot.message(channel, response)
