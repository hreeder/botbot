from redis import StrictRedis


def is_topic_admin(redis, person, topic):
    pass


def create_topic(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    redis.rpush(bot.config['System']['redis_prefix'] + "lists", args[0])
    redis.hmset(bot.config['System']['redis_prefix'] + "lists:%s" % args[0], {"owner": sender})


def destroy_topic(bot, channel, sender, args):
    pass


def allow_sender(bot, channel, sender, args):
    pass


def disallow_sender(bot, channel, sender, args):
    pass


def transfer_topic(bot, channel, sender, args):
    pass


def subscribe(bot, channel, sender, args):
    pass


def unsubscribe(bot, channel, sender, args):
    pass


def broadcast(bot, channel, sender, args):
    subscribers = ["tbrb"]
    topic = args[0]
    message = " ".join(args[1:])
    message = "<BROADCAST to %s> %s: %s" % (topic, sender, message)
    for to in subscribers:
        bot.message(to, message)
