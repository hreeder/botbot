import codecs

from ircbot import bot


@bot.command('rot13')
def rot13(bot, channel, sender, args):
    """
    Usage: {bot.trigget}rot13 <message>

    Applies the Caesar cypher to the string and returns it. Currently only supports rot-13.
    """
    if not args:
        bot.message(channel, f"USAGE: {bot.trigger}rot13 <message>")
        return

    bot.message(channel, "{}: {}".format(sender, codecs.encode(' '.join(args), 'rot-13')))
