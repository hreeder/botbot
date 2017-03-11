import operator

from ircbot import bot
from redis import StrictRedis
from tornado.web import RequestHandler


@bot.command('karma')
def karma_command(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    term = " ".join(args).lower() if args else sender.lower()
    try:
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
    except TypeError:
        amount = "no"
    bot.message(channel, "%s has %s karma" % (term, amount))


def get_multi_karma(bot, number, reverse):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "karma")
    all_karma = [(item[0].decode('utf-8'), int(item[1])) for item in all_karma.items()]
    sorted_karma = sorted(all_karma, key=operator.itemgetter(1), reverse=reverse)

    return sorted_karma[:number]


@bot.command(['top5', 'high5'])
def top_karma(bot, channel, sender, args):
    k = get_multi_karma(bot, 5, True)

    bot.message(channel, ", ".join("%s (%d)" % (item, amount) for item, amount in k))


@bot.command(['last5', 'low5'])
def lowest_karma(bot, channel, sender, args):
    k = get_multi_karma(bot, 5, False)

    bot.message(channel, ", ".join("%s (%d)" % (item, amount) for item, amount in k))


def increment(bot, term):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.hexists(bot.config['System']['redis_prefix'] + "karma", term):
        oldvalue = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        redis.hset(bot.config['System']['redis_prefix'] + "karma", term, oldvalue + 1)
    else:
        redis.hset(bot.config['System']['redis_prefix'] + "karma", term, 1)


def decrement(bot, term):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.hexists(bot.config['System']['redis_prefix'] + "karma", term):
        oldvalue = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        redis.hset(bot.config['System']['redis_prefix'] + "karma", term, oldvalue - 1)
    else:
        redis.hset(bot.config['System']['redis_prefix'] + "karma", term, -1)


@bot.hook()
def message_hook(bot, channel, sender, message):
    redis = None
    term = None

    if message.endswith("++"):
        term = message[:-2].lower()

        if term == sender.lower():
            bot.message(channel, "Haha, nope!")
            decrement(bot, term)
        else:
            increment(bot, term)
    elif message.endswith("--"):
        term = message[:-2].lower()
        decrement(bot, term)

    if term:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        bot.message(channel, "%s now has %s karma" % (term, amount))


@bot.webhook(r"/karma")
class KarmaHandler(RequestHandler):
    def get(self):
        bot = self.application._ctx
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "karma")
        all_karma = {k.decode('utf-8'): int(v) for k, v in all_karma.items()}
        self.write(all_karma)
