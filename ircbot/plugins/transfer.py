import re

from ircbot import bot
from redis import StrictRedis


@bot.command('transfer')
def transfer(bot, channel, sender, args):
    """"command to transfer karma & butts from one term to another"""
    if sender.lower() == bot.config['System']['owner']:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])

        if len(args) == 2:
            old_name = args[0].lower()
            new_name = args[1].lower()
        else:
            string = args.join(" ")
            strings = []
            for term in re.findall("(?![\'\"])[a-z,\s]+(?=[\"\'])", string):
                strings.append(term.strip())
            old_name = strings[0]
            new_name = strings[1]

        # transfer karma
        try:
            old_karma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", old_name))
        except TypeError:
            old_karma = 0
        try:
            new_karma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", new_name))
        except TypeError:
            new_karma = 0
        redis.hset(bot.config['System']['redis_prefix'] + "karma", new_name, old_karma + new_karma)
        redis.hdel(bot.config['System']['redis_prefix'] + "karma", old_name)

        # transfer butts
        try:
            old_butts = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", old_name))
        except TypeError:
            old_butts = 0
        try:
            new_butts = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", new_name))
        except TypeError:
            new_butts = 0
        redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", new_name, new_butts + old_butts)
        redis.hdel(bot.config['System']['redis_prefix'] + "buttmaster", old_name)
        bot.message(channel, "{} now has {} karma and {} butts, {} now has no karma and no butts".format(new_name, 
                                                                                                         old_karma + new_karma,
                                                                                                         old_butts + new_butts,
                                                                                                         old_name))


