from ircbot import bot
from ircbot.webserver import BaseRequestHandler
from redis import StrictRedis


@bot.command('react')
def react(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    term = "_".join(args).lower()
    try:
        url = redis.srandmember(bot.config['System']['redis_prefix'] + "reactions:" + term).decode('utf-8')
        bot.message(channel, url)
    except TypeError:
        pass


@bot.command('addreaction')
def add_reaction(bot, channel, sender, args):
    """ Adds a reaction for a term - usage: {bot.trigger}addreaction http://your.url.here your description here """
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if len(args) == 1:
        bot.message(channel, "You did not specify a description")
    url = args[0]
    term = "_".join(args[1:]).lower()
    redis.sadd(bot.config['System']['redis_prefix'] + "reactions:" + term, url)


@bot.command(';)')
def react_shortcut_eyebrows(bot, channel, sender, args):
    """ Shortcut for {bot.trigger}react eyebrows """
    react(bot, channel, sender, ["eyebrows"])


@bot.webhook(r"/reactions")
class ReactionsHandler(BaseRequestHandler):
    def get(self):
        bot = self.application._ctx
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        prefix = bot.config['System']['redis_prefix'] + "reactions:"

        all_reaction_keys = redis.keys(prefix + "*")
        reactions = {key.decode('utf-8')[len(prefix):]: [item.decode('utf-8') for item in redis.smembers(key)] for key in all_reaction_keys}

        self.write(reactions)
