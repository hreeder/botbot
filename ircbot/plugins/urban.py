import urbandictionary

from ircbot import bot


@bot.command('ud')
def ud(bot, channel, sender, args):
    """ Defines you a word """
    definition = urbandictionary.define(" ".join(args))[0]
    bot.message(channel, "{}: {}".format(
        definition.word,
        definition.definition
    ))


@bot.command('udrandom')
def udrandom(bot, channel, sender, args):
    """ Defines you a random word from urban dictonary"""
    definition = urbandictionary.random()
    bot.message(channel, "{}: {}".format(
        definition[0].word,
        definition[0].definition
    ))
