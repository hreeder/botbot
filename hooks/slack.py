import json
import re
import requests

from redis import StrictRedis


def message_hook(bot, channel, sender, message):
    listen_on = bot.config['Slack']['listen'].split()
    if channel in listen_on and not sender.startswith("["):
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        redis_key = bot.config['System']['redis_prefix'] + "slack-avatar-" + sender

        endpoint = bot.config['Slack']['webhook']
        chanstr = channel.replace("#", "")
        target_channel = bot.config['Slack'][chanstr + "_target"]

        message = message.replace("\x01", "")
        message = re.sub(r'/\[([^@\ ]]+)\]/', r'@$1', message)

        payload = {
            'text': message,
            'username': sender,
            'channel': target_channel
        }

        if redis.exists(redis_key):
            payload['icon_url'] = redis.get(redis_key).decode("utf-8")

        requests.post(endpoint, data=json.dumps(payload))
