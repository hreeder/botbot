import operator

from redis import StrictRedis


def karma_command(bot, channel, sender, args):
    if args:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        term = " ".join(args)
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        bot.message(channel, "%s has %s karma" % (term, amount))

def top_karma(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "karma")
    sorted_karma = sorted(all_karma.items(), key=operator.itemgetter(1), reverse=True)
    items = []

    for item, amount in sorted_karma[0:5]:
        items.append("%s (%s)" % (
            str(item.decode('utf-8')),
            int(amount)
        ))

    bot.message(channel, ", ".join(items))
