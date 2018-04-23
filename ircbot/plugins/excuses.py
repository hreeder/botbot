from redis import StrictRedis

from ircbot import bot, Format


@bot.command('excuse')
def excuseme(bot, channel, sender, args):
    """Usage: {bot.trigger}excuse [excuse_type] - For when you desperately need a good excuse. For a list of excuses try {bot.trigger}excusetypes"""
    excuse_type = "bofh"

    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    excuse_types = redis.keys(bot.config['System']['redis_prefix'] + "excuses:*")
    excuse_types_decoded = [t.decode('utf-8').split(":", 1)[1] for t in excuse_types]

    if len(args) and args[0] in excuse_types_decoded:
        print("Excuse type specified")
        excuse_type = args[0]
    else:
        bot.message(channel, "{}Excuse type {} does not exist, here is an excuse from BOFH{}".format(Format.ROYAL, args[0], Format.RESET))

    print("Excuse: {}".format(excuse_type))
        
    random_excuse = redis.srandmember(bot.config['System']['redis_prefix'] + "excuses:{}".format(excuse_type)).decode('utf-8')

    bot.message(channel, random_excuse)


@bot.command('excusetypes')
def excusetypes(bot, channel, sender, args):
    """Usage: {bot.trigger}excusetypes - Will return a list of valid excuse types"""
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    excuse_types = redis.keys(bot.config['System']['redis_prefix'] + "excuses:*")

    excuse_types_string = ", ".join([t.decode('utf-8').split(":", 1)[1] for t in excuse_types])

    bot.message(channel, "I have the following excuse types: {}".format(excuse_types_string))


@bot.command('addexcuse')
def addexcuse(bot, channel, sender, args):
    """Usage: {bot.trigger}addexcuse [excuse_type] [excuse]"""
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])

    if len(args) < 2:
        bot.message(channel, "This command requires two arguments, {}addexcuse [excuse_type] [excuse]".format(bot.trigger))
        return

    excuse_type = str(args[0])
    excuse = " ".join(args[1:])

    redis.sadd(bot.config['System']['redis_prefix'] + "excuses:" + excuse_type, excuse)

    bot.message(channel, "Excuse added")
