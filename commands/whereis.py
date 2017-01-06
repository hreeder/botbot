import datetime
import json
import requests


def whereis(bot, channel, sender, args):
    """Where Is - Locates someone"""
    who = args[0].lower()
    targets = {
        'rikki': whereis_rikki,
        'r2zer0': whereis_rikki,
        'rhiaro': whereis_amy,
        'amy': whereis_amy,
        'tbrb': whereis_tbrb,
        'harry': whereis_tbrb
    }
    if who in targets.keys():
        targets[who](bot, channel, sender, args)
    elif who == bot.nickname.lower():
        bot.message(channel, "I am in the following places: " + ", ".join(bot.channels.keys()))
    else:
        bot.message(channel, "I do not know this '%s'. If they've got an open API reporting "
                             "their location data, I'd love to know about it though!" % (who,))


def whereis_rikki(bot, channel, sender, args):
    endpoint = "http://gallium.r2zer0.net:5000/"
    mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
    data = json.loads(requests.get(endpoint).text)
    last_updated = datetime.datetime.fromtimestamp(
        int(data['timestamp']) / 1000)
    reported = last_updated.strftime('%Y/%m/%d %H:%M')

    response = "Rikki's last location, reported on %s, was %s%s+%s" % (reported,
                                                                       mapurl,
                                                                       data['latitude'],
                                                                       data['longitude'])

    bot.message(channel, response)


def whereis_tbrb(bot, channel, sender, args):
    endpoint = "http://track-api.harryreeder.co.uk/ehpeeye"
    mapurl = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
    data = json.loads(requests.get(endpoint).text)
    response = "tbrb's last location was %s%s+%s" % (mapurl,
                                                     data['loc']['latitude'], data['loc']['longitude'])
    bot.message(channel, response)


def whereis_amy(bot, channel, sender, args):
    endpoint = "http://rhiaro.co.uk/where"
    data = json.loads(requests.get(endpoint).text)
    bot.message(channel, data['as:summary'] + " - https://rhiaro.co.uk/arrives")
