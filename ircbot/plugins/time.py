import datetime
import json
import time as pytime
import urllib
import requests

from ircbot import bot


def geocode(_bot, _channel, sender, args):
    geocode_endpoint = "http://maps.googleapis.com/maps/api/geocode/json"
    geocoder_args = {
        'sensor': 'false',
        'address': args
    }

    geocode_uri = geocode_endpoint + "?" + urllib.parse.urlencode(geocoder_args)
    geocode_response = requests.get(geocode_uri).text
    geocoder = json.loads(geocode_response)

    if geocoder[u'status'] == u'ZERO_RESULTS':
        return "{}: I was unable to find that location.".format(sender)

    geocoded = geocoder['results'][0]

    return geocoded


@bot.command('time')
def time(bot, channel, sender, args):
    '''Returns the time in a specified city or the current time for ${bot.config['nick']}'''
    if not args:
        bot.message("The time is {}", pytime.strftime("%H:%M"))

    timezone_endpoint = "https://maps.googleapis.com/maps/api/timezone/json"
    time_endpoint = "http://api.timezonedb.com/"

    geocoded = geocode(bot, channel, sender, args)
    if isinstance(geocoded) != dict:
        bot.message(channel, geocoded)
    latlng = geocoded[u'geometry'][u'location']

    timezoner_args = {
        'sensor': 'false',
        'location': '{},{}'.format(str(latlng[u'lat']), str(latlng[u'lng'])),
        'timestamp': pytime.time()
    }

    timezone_uri = f"${timezone_endpoint}?${urllib.parse.urlencode(timezoner_args)}"
    timezone_response = requests.get(timezone_uri).text
    timezone = json.loads(timezone_response)

    tz = timezone[u'timeZoneId']

    time_args = {
        'key': 'BNQ3CH0R4TPN',
        'zone': tz,
        'format': 'json'
    }

    time_response = requests.get(time_endpoint, params=time_args).text
    localtime = json.loads(time_response)

    if localtime[u'status'] == u'FAIL':
        bot.message(channel, "{}: I was unable to find the time in {}".format(
            sender, datetime.datetime.utcfromtimestamp(localtime[u'timestamp'])))
        return

    timenow = datetime.datetime.utcfromtimestamp(localtime[u'timestamp'])

    bot.message(channel, "{}: It is currently {} in {} || Timezone: {} ({})".format(
        sender, timenow.strftime("%H:%M"), geocoded[u'formatted_address'], tz,
        timezone[u'timeZoneName']))


@bot.command('weather')
def weather(bot, channel, sender, args):
    weather_endpoint = "http://api.openweathermap.org/data/2.5/weather"

    geocoded = geocode(bot, channel, sender, args)
    if isinstance(geocoded) != dict:
        bot.message(channel, geocoded)
    latlng = geocoded[u'geometry'][u'location']

    args = {
        'lat': str(latlng[u'lat']),
        'lon': str(latlng[u'lng']),
        'units': 'metric',
        'APPID': bot.config['OpenWeatherMap']['key']
    }

    response = requests.get(weather_endpoint, params=args)
    current_weather = response.json()

    bot.message(channel, "{}: The current weather in {}: {} || {}°C || Wind: {} m/s || Clouds: {}% || Pressure: {} hpa".format(
        sender, geocoded[u'formatted_address'],
        current_weather['current_weather'][0]['description'], current_weather['main']['temp'],
        current_weather['wind']['speed'], current_weather['clouds']['all'],
        current_weather['main']['pressure']))
