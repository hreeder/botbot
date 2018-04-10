import re

from ircbot import bot
from redis import StrictRedis


@bot.command('transfer')
def transfer(bot, channel, sender, args):
    """"command to transfer karma & butts from one term to another, usage: $transfer name1 name2"""
    if sender.lower() == bot.config['System']['owner']:
        if len(args) == 2:
                first_name = args[0].lower()
                second_name = args[1].lower()
        else:
            string = " ".join(args)
            strings = []
            for term in re.findall("(?![\'\"])[a-z,\s]+(?=[\"\'])", string):
                strings.append(term.strip())
            try:
                first_name = strings[0].lower()
                second_name = strings[1].lower()
            except IndexError:
                bot.message(channel, "Oops! Looks like you didn't give enough arguments!, please use the following syntax: `$transfer name1 name2` ")
                return

        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        # transfer karma
        try:
            first_karma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", first_name))
        except TypeError:
            first_karma = 0
        try:
            second_karma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", second_name))
        except TypeError:
            second_karma = 0
        redis.hset(bot.config['System']['redis_prefix'] + "karma", second_name, first_karma + second_karma)
        redis.hdel(bot.config['System']['redis_prefix'] + "karma", first_name)

        # transfer butts
        try:
            first_butts = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", first_name))
        except TypeError:
            first_butts = 0
        try:
            second_butts = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", second_name))
        except TypeError:
            second_butts = 0
        redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", second_name, second_butts + first_butts)
        redis.hdel(bot.config['System']['redis_prefix'] + "buttmaster", first_name)

        bot.message(channel, "{} now has {} karma and {} butts, {} now has no karma and no butts".format(second_name,
                                                                                                         first_karma + second_karma,
                                                                                                         first_butts + second_butts,
                                                                                                         first_name))
