import random

from ircbot import bot


@bot.command("shipit")
def shipit(bot, channel, sender, args):
    """Usage: {bot.trigger}shipit - Ship it squirrel"""
    bot.message(channel, random.choice([
        "http://shipitsquirrel.github.io/images/ship%20it%20squirrel.png",
        "http://media.tumblr.com/tumblr_lybw63nzPp1r5bvcto1_500.jpg",
        "http://i.imgur.com/DPVM1.png",
        "http://d2f8dzk2mhcqts.cloudfront.net/0772_PEW_Roundup/09_Squirrel.jpg",
        "http://www.cybersalt.org/images/funnypictures/s/supersquirrel.jpg",
        "http://www.zmescience.com/wp-content/uploads/2010/09/squirrel.jpg",
        "https://dl.dropboxusercontent.com/u/602885/github/sniper-squirrel.jpg",
        "http://1.bp.blogspot.com/_v0neUj-VDa4/TFBEbqFQcII/AAAAAAAAFBU/E8kPNmF1h1E/s640/squirrelbacca-thumb.jpg",
        "https://dl.dropboxusercontent.com/u/602885/github/soldier-squirrel.jpg",
        "https://dl.dropboxusercontent.com/u/602885/github/squirrelmobster.jpeg",
    ]))
