import datetime
import json
import requests


def whereis(bot, channel, sender, args):
    """Where Is - Locates someone"""
    who = args[0].lower()
    targets = {
        'rikki': whereis_rikki,
        'r2zer0': whereis_rikki
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
        int(data['timestamp'])/1000)

    response = "Rikki's last location, reported on %d/%d/%d %d:%d, was " % (last_updated.year,
                                                                            last_updated.month,
                                                                            last_updated.day,
                                                                            last_updated.hour,
                                                                            last_updated.minute)
    response += mapurl + "%s+%s" % (data['latitude'],
                                    data['longitude'])

    bot.message(channel, response)