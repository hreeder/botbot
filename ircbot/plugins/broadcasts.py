from ircbot import bot
from redis import StrictRedis


@bot.command('broadcast-topic-create')
def create_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if not redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.hmset(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), {"owner": sender})
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic), sender)
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:{}:senders".format(topic), sender)
        bot.message(channel, "{}: New topic '{}' created, with yourself as the owner. You have also been subscribed to the topic by default.".format(sender, topic))
    else:
        owner = redis.hget(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner").decode('utf-8')
        bot.message(channel, "{}: The topic '{}' already exists, and is owned by {}.".format(sender, topic, owner))


@bot.command('broadcast-topic-destroy')
def destroy_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner").decode('utf-8'):
        redis.srem(bot.config['System']['redis_prefix'] + "lists", topic)
        redis.delete(bot.config['System']['redis_prefix'] + "lists:{}".format(topic))
        redis.delete(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic))
        redis.delete(bot.config['System']['redis_prefix'] + "lists:{}:senders".format(topic))
        bot.message(channel, "{}: Topic '{}' was destroyed".format(sender, topic))
    else:
        bot.message(channel, "{}: You are not the owner of the topic '{}' and thus cannot destroy it".format(sender, topic))


@bot.command('broadcast-topic-allow')
def allow_sender(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner").decode('utf-8'):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:{}:senders".format(topic), args[1])
        bot.message(channel, "{}: You have now given {} the ability to broadcast to the topic '{}'".format(sender, args[1], topic))
    else:
        bot.message(channel, "{}: You are not the owner of the topic '{}' and cannot add people to the senders list".format(sender, topic))


@bot.command('broadcast-topic-revoke')
def disallow_sender(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner").decode('utf-8'):
        redis.srem(bot.config['System']['redis_prefix'] + "lists:{}:senders".format(topic), args[1])
        bot.message(channel, "{}: You have now removed the ability to broadcast to the topic '{}' from {}".format(sender, topic, args[1]))
    else:
        bot.message(channel, "{}: You are not the owner of the topic '{}' and cannot add people to the senders list".format(sender, topic))


@bot.command('broadcast-topic-transfer')
def transfer_topic(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if sender == redis.hget(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner").decode('utf-8') and args[1]:
        redis.hset(bot.config['System']['redis_prefix'] + "lists:{}".format(topic), "owner", args[1])
        bot.message(channel, "{}: You have now transferred ownership of the topic '{}' to {}".format(sender, topic, args[1]))
    else:
        bot.message(channel, "{}: You are not the owner of the topic '{}' and cannot transfer ownership of it.".format(sender, topic))


@bot.command('subscribe')
def subscribe(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
        redis.sadd(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic), sender)
        bot.message(channel, "{}: You are now subscribed to the topic '{}'".format(sender, topic))
    else:
        bot.message(channel, "{}: You cannot subscribe to a topic that doesn't exist!".format(sender))


@bot.command('unsubscribe')
def unsubscribe(bot, channel, sender, args):
    topic = args[0]
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic) and redis.sismember(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic), sender):
        redis.srem(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic), sender)
        bot.message(channel, "{}: You have now been unsubscribed from the topic '{}'".format(sender, topic))
    else:
        bot.message(channel, "{}: Either that topic does not exist, or you are not a subscriber, and thus cannot unsubscribe from it!".format(sender))


@bot.command('bc')
def broadcast(bot, channel, sender, args):
    topic = args[0]

    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic) and redis.sismember(bot.config['System']['redis_prefix'] + "lists:{}:senders".format(topic), sender):
        subscribers = redis.smembers(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic))
        message = " ".join(args[1:])
        message = "<BROADCAST to {}> {}: {}".format(topic, sender, message)
        bot.message(channel, "{}: Sending broadcast to {:d} subscriber(s) of '{}'".format(sender, len(subscribers), topic))
        for to in subscribers:
            bot.message(to.decode('utf-8'), message)
    else:
        if redis.sismember(bot.config['System']['redis_prefix'] + "lists", topic):
            bot.message(channel, "{}: You cannot send to that topic!".format(sender))
        else:
            bot.message(channel, "{}: Cannot send to a topic that doesn't exist!".format(sender))


@bot.command('subscriptions')
def list_topics(bot, channel, sender, args):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    subscribed_topics = []
    topics = redis.smembers(bot.config['System']['redis_prefix'] + "lists")
    for topic in topics:
        topic = topic.decode('utf-8')
        if redis.sismember(bot.config['System']['redis_prefix'] + "lists:{}:subscribers".format(topic), sender):
            subscribed_topics.append(topic)
    bot.message(channel, "{}: You are subscribed to the following topics: {}".format(sender, ", ".join(subscribed_topics)))
