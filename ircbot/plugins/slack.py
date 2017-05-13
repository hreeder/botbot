import hashlib
import json
import re
import requests

from ircbot import bot
from redis import StrictRedis
from slacker import Slacker


@bot.command('slackwho')
def slackwho(bot, channel, sender, args):
    """SlackWho will PM you a list of all users of the associated Slack Team"""
    slacker = Slacker(bot.config['Slack']['api_key'])
    users_response = slacker.users.list(presence=True)
    users = [user['name'] for user in users_response.body['members']]
    users.reverse()

    while users:
        outlist = []
        try:
            for n in range(0, 10):
                outlist.append(users.pop())
        except IndexError:
            pass
        output = "Slack Users: %s " % ", ".join(outlist)
        bot.message(sender, output)


@bot.command('slackwhois')
def slackwhois(bot, channel, sender, args):
    """SlackWhois will return Username, Real Name (if available) and presence information about a given Slack user"""
    slacker = Slacker(bot.config['Slack']['api_key'])
    if not args:
        bot.message(channel, "%s: Please supply a user to look up" % sender)
        return
    users_response = slacker.users.list(presence=True)
    users = {user['name']: user for user in users_response.body['members']}

    if args[0] not in users:
        bot.message(channel, "%s: %s was not found in the slack team" % (sender, args[0]))
        return

    user = args[0]
    user = users[user]

    name_str = user['name']
    if user['profile']['real_name']:
        name_str += " (%s)" % user['profile']['real_name']

    bot.message(channel, "Slack User: %s, Presence: %s" % (name_str, user['presence']))


@bot.command('slacksetavatar')
def slacksetavatar(bot, channel, sender, args):
    """SlackSetAvatar will set the avatar associated with your nickname.
    You can pass in either a URL or an E-Mail address (to use Gravatar)"""
    if args:
        inp = args[0]
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        if inp.startswith("http://") or inp.startswith("https://"):
            # we're dealing with a direct url, store it
            redis.set(bot.config['System']['redis_prefix'] + "slack-avatar-" + sender, inp)
            bot.message(sender, "Ok, I've set that for you. Your avatar URL is: " + inp)
            return
        elif "@" in inp:
            # We're dealing with an email, let's treat it as gravatar
            url = "http://www.gravatar.com/avatar/" + hashlib.md5(inp.encode('utf-8').lower()).hexdigest() + "?s=200"
            redis.set(bot.config['System']['redis_prefix'] + "slack-avatar-" + sender, url)
            bot.message(sender, "Ok, I've set that for you. Your avatar URL is: " + url)
            return
        else:
            bot.message(sender, "Sorry, that wasn't recognised. I can support setting an email for gravatar "
                        "or a direct url for an avatar")


@bot.hook()
def message_hook(bot, channel, sender, message):
    listen_on = bot.config['Slack']['listen'].split()
    if channel in listen_on and not sender.startswith("["):
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        redis_key = bot.config['System']['redis_prefix'] + "slack-avatar-" + sender

        slacker = Slacker(bot.config['Slack']['api_key'])

        endpoint = bot.config['Slack']['webhook']
        chanstr = channel.replace("#", "")
        target_channel = bot.config['Slack'][chanstr + "_target"]

        message = message.replace("\x01", "")
        message = re.sub(r'/\[([^@\ ]]+)\]/', r'@$1', message)

        payload = {
            'text': message,
            'username': sender,
            'channel': target_channel,
            'as_user': False
        }

        avatar = None

        if redis.exists(redis_key):
            avatar = redis.get(redis_key).decode("utf-8")

#        print(payload)

#        requests.post(endpoint, data=json.dumps(payload))
        slacker.chat.post_message(target_channel, text=message, username=sender, as_user=False, icon_url=avatar)
