from redis import StrictRedis


def message_hook(bot, channel, sender, message):
    if "butt" in message.lower() and sender not in ['buttbot']:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])

        if redis.hexists(bot.config['System']['redis_prefix'] + "buttmaster", sender):
            current = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", sender))
            redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", sender, current + 1)
        else:
            redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", sender, 1)
