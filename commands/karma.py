import operator

from redis import StrictRedis


def karma_command(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    term = " ".join(args).lower() if args else sender
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


def top_karma(bot, channel, sender, args):
    k = get_multi_karma(bot, 5, True)

    bot.message(channel, ", ".join("%s (%d)" % (item, amount) for item, amount in k))


def lowest_karma(bot, channel, sender, args):
    k = get_multi_karma(bot, 5, False)

    bot.message(channel, ", ".join("%s (%d)" % (item, amount) for item, amount in k))
