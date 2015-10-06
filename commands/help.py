def help(bot, channel, sender, args):
    """Shows all commands, or gets help for a specific command"""
    if args and args[0] in bot.commands.keys():
        docstring = bot.commands[args[0]].__doc__
        bot.message(channel, "Help for {0}: {1}".format(args[0], docstring))
    else:
        bot.message(channel, "I know the following channel commands: {0} "
                             "(Note other commands may be available in PMs)".format(", ".join(sorted(bot.commands.keys()))))


def help_pm(bot, sender, args):
    """Shows all commands, or gets help for a specific command"""
    if args and args[0] in bot.pm_commands.keys():
        docstring = bot.pm_commands[args[0]].__doc__
        bot.message(sender, "Help for {0}: {1}".format(args[0], docstring))
    else:
        bot.message(sender, "I know the following PM commands (Note some of these "
                            "are for the bot owner only): {0}".format(", ".join(sorted(bot.pm_commands.keys()))))


def bot_info(bot, channel, sender, args):
    """Returns info about the bot, it's owner and where to report issues"""
    bot.message(channel, "%s: I am %s, a deployment of BotBot. My owner is %s. Any issues can be reported at %s" % (
        sender,
        bot.config['IRC']['nick'],
        bot.config['System']['owner'],
        bot.config['System']['repo']
    ))