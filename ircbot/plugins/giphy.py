from giphypop import screensaver

from ircbot import bot


@bot.command('giphy')
def giphy(bot, channel, sender, args):
    """Usage: {bot.trigger}giphy [tag] - Finds a random gif, or returns a random gif tagged with [tag]"""
    tag = None
    if args:
        tag = " ".join(args)
    bot.message(channel, screensaver(tag=tag).fixed_height.url)
