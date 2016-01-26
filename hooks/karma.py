from redis import StrictRedis


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


def message_hook(bot, channel, sender, message):
    redis = None
    term = None

    if message.endswith("++"):
        term = message[:-2]

        if term == sender:
            bot.message(channel, "Haha, nope!")
            decrement(bot, term)
        else:
            increment(bot, term)
    elif message.endswith("--"):
        term = message[:-2]
        decrement(bot, term)

    if term:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        amount = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", term))
        bot.message(channel, "%s now has %s karma" % (term, amount))
