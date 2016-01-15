from redis import StrictRedis


def message_hook(bot, channel, sender, message):
    redis = None
    term = None

    if message.endswith("++"):
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        term = message[:-2]

        if redis.hexists(bot.config['System']['redis_prefix'] + "karma", term):
            oldvalue = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
            redis.hset(bot.config['System']['redis_prefix'] + "karma", term, oldvalue + 1)
        else:
            redis.hset(bot.config['System']['redis_prefix'] + "karma", term, 1)
    elif message.endswith("--"):
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        term = message[:-2]

        if redis.hexists(bot.config['System']['redis_prefix'] + "karma", term):
            oldvalue = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
            redis.hset(bot.config['System']['redis_prefix'] + "karma", term, oldvalue - 1)
        else:
            redis.hset(bot.config['System']['redis_prefix'] + "karma", term, -1)

    if redis:
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        bot.message(channel, "%s now has %s karma" % (term, amount))
