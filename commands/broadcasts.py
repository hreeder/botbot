from redis import StrictRedis


def is_topic_admin(redis, person, topic):
    pass


def create_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if not redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.hmset(bot.config['System']['redis_prefix'] + "lists:%s" % topic, {"owner": sender})
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender)
        bot.message(channel, "%s: New topic '%s' created, with yourself as the owner. You have also been subscribed to the topic by default." % (sender, topic))
    else:
        owner = redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8')
        bot.message(channel, "%s: The topic '%s' already exists, and is owned by %s." % (sender, topic, owner))


def destroy_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8'):
        redis.srem(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:%s" % topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic)
        bot.message(channel, "%s: Topic '%s' was destroyed" % (sender, topic))
    else:
        bot.message(channel, "%s: You are not the owner of the topic '%s' and thus cannot destroy it" % (sender, topic))


def allow_sender(bot, channel, sender, args):
    pass


def disallow_sender(bot, channel, sender, args):
    pass


def transfer_topic(bot, channel, sender, args):
    pass


def subscribe(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender)
        bot.message(channel, "%s: You are now subscribed to the topic '%s'" % (sender, topic))
    else:
        bot.message(channel, "%s: You cannot subscribe to a topic that doesn't exist!" % sender)


def unsubscribe(bot, channel, sender, args):
    pass


def broadcast(bot, channel, sender, args):
    topic = args[0]
    
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        subscribers = redis.smembers(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic)
        print(subscribers)
        message = " ".join(args[1:])
        message = "<BROADCAST to %s> %s: %s" % (topic, sender, message)
        bot.message(channel, "%s: Sending broadcast to %d subscriber(s) of '%s'" % (sender, len(subscribers), topic))
        for to in subscribers:
            bot.message(to.decode('utf-8'), message)
    else:
        bot.message(channel, "%s: Cannot send to a topic that doesn't exist!" % sender)
