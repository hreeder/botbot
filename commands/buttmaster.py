import operator

from redis import StrictRedis


def buttmaster(bot, channel, sender, args):
    if args and int(args[0]):
        top = get_multi_butts(bot, int(args[0]), True)
        bot.message(channel, ", ".join("%s (%d)" % (item, amount) for item, amount in top))
    else:
        top = get_multi_butts(bot, 1, True)[0]
        bot.message(channel, "The buttmaster is %s, with %s butts" % (top[0], top[1]))


def butts(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    who = " ".join(args).lower() if args else sender
    try:
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", who))
    except TypeError:
        amount = "no"

    bot.message(channel, "%s has %s butts" % (who, amount))


def get_multi_butts(bot, number, reverse):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "buttmaster")
    all_karma = [(item[0].decode('utf-8'), int(item[1])) for item in all_karma.items()]
    sorted_karma = sorted(all_karma, key=operator.itemgetter(1), reverse=reverse)

    return sorted_karma[:number]
