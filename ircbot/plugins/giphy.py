from giphypop import screensaver

from ircbot import bot


@bot.command('giphy')
def giphy(bot, channel, sender, args):
    tag = None
    if args:
        tag = " ".join(args)
    bot.message(channel, screensaver(tag=tag).fixed_height.url)
