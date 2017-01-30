from ircbot import bot
from redis import StrictRedis


@bot.command('broadcast-topic-create')
def create_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if not redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.hmset(bot.config['System']['redis_prefix'] + "lists:%s" % topic, {"owner": sender})
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender)
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:senders" % topic, sender)
        bot.message(channel, "%s: New topic '%s' created, with yourself as the owner. You have also been subscribed to the topic by default." % (sender, topic))
    else:
        owner = redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8')
        bot.message(channel, "%s: The topic '%s' already exists, and is owned by %s." % (sender, topic, owner))


@bot.command('broadcast-topic-destroy')
def destroy_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8'):
        redis.srem(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:%s" % topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:%s:senders" % topic)
        bot.message(channel, "%s: Topic '%s' was destroyed" % (sender, topic))
    else:
        bot.message(channel, "%s: You are not the owner of the topic '%s' and thus cannot destroy it" % (sender, topic))


@bot.command('broadcast-topic-allow')
def allow_sender(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8'):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:senders" % topic, args[1])
        bot.message(channel, "%s: You have now given %s the ability to broadcast to the topic '%s'" % (sender, args[1], topic))
    else:
        bot.message(channel, "%s: You are not the owner of the topic '%s' and cannot add people to the senders list" % (sender, topic))


@bot.command('broadcast-topic-revoke')
def disallow_sender(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8'):
        redis.srem(bot.config['System']['redis_prefix'] + "lists:%s:senders" % topic, args[1])
        bot.message(channel, "%s: You have now removed the ability to broadcast to the topic '%s' from %s" % (sender, topic, args[1]))
    else:
        bot.message(channel, "%s: You are not the owner of the topic '%s' and cannot add people to the senders list" % (sender, topic))


@bot.command('broadcast-topic-transfer')
def transfer_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner").decode('utf-8') and args[1]:
        redis.hset(bot.config['System']['redis_prefix'] + "lists:%s" % topic, "owner", args[1])
        bot.message(channel, "%s: You have now transferred ownership of the topic '%s' to %s" % (sender, topic, args[1]))
    else:
        bot.message(channel, "%s: You are not the owner of the topic '%s' and cannot transfer ownership of it." % (sender, topic))


@bot.command('subscribe')
def subscribe(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender)
        bot.message(channel, "%s: You are now subscribed to the topic '%s'" % (sender, topic))
    else:
        bot.message(channel, "%s: You cannot subscribe to a topic that doesn't exist!" % sender)


@bot.command('unsubscribe')
def unsubscribe(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic) and redis.sismember(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender):
        redis.srem(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender)
        bot.message(channel, "%s: You have now been unsubscribed from the topic '%s'" % (sender, topic))
    else:
        bot.message(channel, "%s: Either that topic does not exist, or you are not a subscriber, and thus cannot unsubscribe from it!" % sender)


@bot.command('bc')
def broadcast(bot, channel, sender, args):
    topic = args[0]

    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic) and redis.sismember(bot.config['System']['redis_prefix'] + "lists:%s:senders" % topic, sender):
        subscribers = redis.smembers(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic)
        message = " ".join(args[1:])
        message = "<BROADCAST to %s> %s: %s" % (topic, sender, message)
        bot.message(channel, "%s: Sending broadcast to %d subscriber(s) of '%s'" % (sender, len(subscribers), topic))
        for to in subscribers:
            bot.message(to.decode('utf-8'), message)
    else:
        if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
            bot.message(channel, "%s: You cannot send to that topic!" % sender)
        else:
            bot.message(channel, "%s: Cannot send to a topic that doesn't exist!" % sender)


@bot.command('subscriptions')
def list_topics(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    subscribed_topics = []
    topics = redis.smembers(bot.config['System']['redis_prefix'] + "lists")
    for topic in topics:
        topic = topic.decode('utf-8')
        if redis.sismember(bot.config['System']['redis_prefix'] + "lists:%s:subscribers" % topic, sender):
            subscribed_topics.append(topic)
    bot.message(channel, "%s: You are subscribed to the following topics: %s" % (sender, ", ".join(subscribed_topics)))
