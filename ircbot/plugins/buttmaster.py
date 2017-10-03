import operator

from ircbot import bot
from redis import StrictRedis


@bot.command('buttmaster')
def buttmaster(bot, channel, sender, args):
    if args and int(args[0]):
        top = get_multi_butts(bot, int(args[0]), True)
        bot.message(channel, ", ".join("{} {:d}".format(item, amount) for item, amount in top))
    else:
        top = get_multi_butts(bot, 1, True)[0]
        bot.message(channel, "The buttmaster is {}, with {} butts".format(top[0], top[1]))


@bot.command('butts')
def butts(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    who = " ".join(args).lower() if args else sender
    try:
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", who))
    except TypeError:
        amount = "no"

    bot.message(channel, "{} has {} butts".format(who, amount))


def get_multi_butts(bot, number, reverse):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "buttmaster")
    all_karma = [(item[0].decode('utf-8'), int(item[1])) for item in all_karma.items()]
    sorted_karma = sorted(all_karma, key=operator.itemgetter(1), reverse=reverse)

    return sorted_karma[:number]


@bot.hook()
def message_hook(bot, channel, sender, message):
    if "butt" in message.lower() and sender not in ['buttbot']:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])

        if redis.hexists(bot.config['System']['redis_prefix'] + "buttmaster", sender):
            current = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", sender))
            redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", sender, current + 1)
        else:
            redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", sender, 1)
