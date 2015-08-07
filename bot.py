import datetime
import json
import logging
import pylast
import requests

from irc import IRC
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

if config['System'].getboolean('debug'):
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

if "trigger" in config['IRC']:
    trigger = config['IRC']['trigger']
else:
    trigger = "$"

irc = IRC(host=config['IRC']['host'],
          port=config['IRC']['port'],
          nick=config['IRC']['nick'],
          channel=config['IRC']['channel'])


def main():
    irc.channel_message_received_callback = channel_message
    irc.start_connection()


def channel_message(sender, channel, message):
    if config['System']['debug']:
        logger.debug("[{0}] {1}: {2}".format(channel, sender, message))

    if message.startswith(trigger):
        # T R I G G E R E D
        message = message[len(trigger):].strip()
        command = message.split(" ")[0]
        args = message.split(" ")[1:]
        logger.debug("Message: " + message)
        logger.debug("Command: " + command)
        logger.debug("Args: " + " ".join(args))

        if command == "whereis" and args:
            who = args[0].lower()
            rikki = ["rikki", "r2zer0"]
            if who in rikki:
                endpoint = "http://gallium.r2zer0.net:5000/whereisrikki"
                map = "http://maps.googleapis.com/maps/api/staticmap?size=640x320&markers=size:large%7Ccolor:0xc0c0c0%7C"
                data = json.loads(requests.get(endpoint).text)
                last_updated = datetime.datetime.fromtimestamp(
                    int(data['timestamp'])/1000)

                response = "Rikki's last location, reported on %d/%d/%d %d:%d, was " % (last_updated.year,
                                                                                        last_updated.month,
                                                                                        last_updated.day,
                                                                                        last_updated.hour,
                                                                                        last_updated.minute)
                response += map + "%s+%s" % (data['latitude'],
                                             data['longitude'])

                irc.send_channel_message(channel, response)
            else:
                irc.send_channel_message(channel,
                                         "I do not know this '%s'. If they've got an open API reporting their latitude and longitude, I'd love to know about it though!" % (who,))

        elif command == "np":
            if args:
                user = args[0].strip()
            else:
                user = sender
            logger.debug("User: " + user)
            network = pylast.LastFMNetwork(
                api_key=config['LastFM']['key'],
                api_secret=config['LastFM']['secret']
            )

            try:
                user = network.get_user(user)
                np = user.get_now_playing()
                if np:
                    irc.send_channel_message(channel, "[LastFM] %s is currently listening to '%s'" % (user.get_name(), np))
                else:
                    irc.send_channel_message(channel, "[LastFM] %s is not currently scrobbling" % user.get_name())
            except pylast.WSError:
                    irc.send_channel_message(channel, "[LastFM] I cannot find the user '%s'" % user)


if __name__ == '__main__':
    main()
