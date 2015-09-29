import json
import re
import requests


def message_hook(bot, channel, sender, message):
    listen_on = bot.config['Slack']['listen'].split()
    if channel in listen_on and not sender.startswith("["):
        print(channel, sender, message)
        endpoint = bot.config['Slack']['webhook']
        chanstr = channel.replace("#","")
        target_channel = bot.config['Slack'][chanstr+"_target"]

        message = message.replace("\x01", "")
        message = re.sub(r'/\[([^@\ ]]+)\]/', r'@$1', message)

        payload = {
            'text': message,
            'username': sender,
            'channel': target_channel
        }

        postit = requests.post(
            endpoint,
            data=json.dumps(payload)
        )
