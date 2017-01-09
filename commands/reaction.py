from redis import StrictRedis


def react(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    term = "_".join(args).lower()
    try:
        url = redis.srandmember(bot.config['System']['redis_prefix'] + "reactions:" + term).decode('utf-8')
        bot.message(channel, url)
    except TypeError:
        pass


def add_reaction(bot, channel, sender, args):
    """ Adds a reaction for a term - usage: $addreaction http://your.url.here your description here """
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if len(args) == 1:
        bot.message(channel, "You did not specify a description")
    url = args[0]
    term = "_".join(args[1:]).lower()
    redis.sadd(bot.config['System']['redis_prefix'] + "reactions:" + term, url)
