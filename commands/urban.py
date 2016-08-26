import urbandictionary


def ud(bot, channel, sender, args):
    """ Defines you a word """
    definition = urbandictionary.define(" ".join(args))[0]
    bot.message(channel, "{}: {}".format(
        definition.word,
        definition.definition
    ))
