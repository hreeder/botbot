import subprocess as sp

from ircbot import bot


@bot.command('ping')
def ipcheck(bot, channel, sender, args):
    """Ping a host. Usage: $ping example.com"""
    ip = args[0]
    status, result = sp.getstatusoutput("ping -c1 -w2 " + str(ip))
    if status == 0:
        bot.message(channel, "Host " + str(ip) + " is Up!")
    else:
        bot.message(channel, "Host " + str(ip) + " is Down!")


