import datetime
import json
import requests


def whereis(bot, channel, sender, args):
    """Where Is - Locates someone"""
    who = args[0].lower()
    rikki = ["rikki", "r2zer0"]
    if who in rikki:
        endpoint = "http://gallium.r2zer0.net:5000/whereisrikki"
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
    elif who == bot.nickname.lower():
        bot.message(channel, "I am in the following places: " + ", ".join(bot.channels.keys()))
    else:
        bot.message(channel, "I do not know this '%s'. If they've got an open API reporting "
                             "their latitude and longitude, I'd love to know about it though!" % (who,))