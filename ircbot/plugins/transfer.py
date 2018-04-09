import re

from ircbot import bot
from redis import StrictRedis

@bot.command('transfer')
def transfer(bot, channel, sender, args):
    """"command to transfer karma & butts from one term to another"""
    if sender.lower() == bot.config['System']['owner']:
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        oldname = args[0].lower()
        newname = args[1].lower()

        #transfer karma
        try:
            oldkarma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", oldname))
        except TypeError:
            oldkarma = 0
        try:
            newkarma = int(redis.hget(bot.config['System']['redis_prefix'] + "karma", newname))
        except TypeError:
            newkarma = 0
        redis.hset(bot.config['System']['redis_prefix'] + "karma", newname, oldkarma + newkarma)
        redis.hdel(bot.config['System']['redis_prefix'] + "karma", oldname)

        #transfer butts
        try:
            oldbutts = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", oldname))
        except TypeError:
            oldbutts = 0
        try:
            newbutts = current = int(redis.hget(bot.config['System']['redis_prefix'] + "buttmaster", newname))
        except TypeError:
            newbutts = 0
        redis.hset(bot.config['System']['redis_prefix'] + "buttmaster", newname, newbutts + oldbutts)
        redis.hdel(bot.config['System']['redis_prefix'] + "buttmaster", oldname)


