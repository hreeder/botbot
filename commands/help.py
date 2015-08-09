def help(bot, channel, sender, args):
    bot.message(channel, "I know the following channel commands: {0}".format(", ".join(bot.commands.keys())))


def help_pm(bot, sender, args):
    bot.message(sender, "I know the following PM commands (Note some of these "
                        "are for the bot owner only): {0}".format(", ".join(bot.pm_commands.keys())))