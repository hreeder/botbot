import datetime
import json
import time as pytime
import urllib
import requests


def geocode(bot, channel, sender, args):
    geocode_endpoint = "http://maps.googleapis.com/maps/api/geocode/json"
    geocoder_args = {
        'sensor': 'false',
        'address': args
    }

    geocode_uri = geocode_endpoint + "?" + urllib.parse.urlencode(geocoder_args)
    geocode_response = requests.get(geocode_uri).text
    geocoder = json.loads(geocode_response)

    if geocoder[u'status'] == u'ZERO_RESULTS':
        return "%s: I was unable to find that location." % (sender,)

    geocoded = geocoder['results'][0]

    return geocoded


def time(bot, channel, sender, args):
    '''Returns the time in a specified city'''
    timezone_endpoint = "https://maps.googleapis.com/maps/api/timezone/json"
    time_endpoint = "http://api.timezonedb.com/"

    geocoded = geocode(bot, channel, sender, args)
    if type(geocoded) != dict:
        bot.message(channel, geocoded)
    latlng = geocoded[u'geometry'][u'location']

    timezoner_args = {
        'sensor': 'false',
        'location': str(latlng[u'lat']) + ',' + str(latlng[u'lng']),
        'timestamp': pytime.time()
    }

    timezone_uri = timezone_endpoint + "?" + \
        urllib.parse.urlencode(timezoner_args)
    timezone_response = requests.get(timezone_uri).text
    timezone = json.loads(timezone_response)

    tz = timezone[u'timeZoneId']

    time_args = {
        'key': 'BNQ3CH0R4TPN',
        'zone': tz,
        'format': 'json'
    }

    time_uri = time_endpoint + "?" + urllib.parse.urlencode(time_args)
    time_response = requests.get(time_uri).text
    localtime = json.loads(time_response)

    if localtime[u'status'] == u'FAIL':
        bot.message(channel, "%s: I was unable to find the time in %s" % (sender, datetime.datetime.utcfromtimestamp(localtime[u'timestamp'])))
        return

    timenow = datetime.datetime.utcfromtimestamp(localtime[u'timestamp'])

    bot.message(channel, "%s: It is currently %s in %s || Timezone: %s (%s)" % (sender,
                                                                                timenow.strftime("%H:%M"),
                                                                                geocoded[u'formatted_address'],
                                                                                tz,
                                                                                timezone[u'timeZoneName']))
