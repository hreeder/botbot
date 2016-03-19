def die(bot, sender, args):
    """Owner Command: Causes the bot to disconnect"""
    if sender == bot.config['System']['owner'] and args and args[0] == bot.config['System']['die_password']:
        bot.disconnect()


def nick(bot, sender, args):
    """Owner Command: Causes the bot to change it's nick"""
    if sender == bot.config['System']['owner'] and args:
        bot.set_nickname(args[0])


def join(bot, sender, args):
    """Owner Command: Causes the bot to join a channel"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        if len(args) > 1:
            # Channel has a password
            bot.join(args[0], password=args[1])
        else:
            bot.join(args[0])


def part(bot, sender, args):
    """Owner Command: Causes the bot to part a channel"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        message = None
        if len(args) > 1:
            message = args[1]
        if bot.in_channel(args[0]):
            bot.part(args[0], message=message)


def message(bot, sender, args):
    """Owner Command: Sends a message to a channel as the bot"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        message = " ".join(args[1:])
        bot.message(args[0], message)


def channel_ignore(bot, channel, sender, args):
    ignore(bot, sender, args)


def ignore(bot, sender, args):
    if sender == bot.config['System']['owner'] and args:
        bot.ignored_users.add(args[0])


def channel_unignore(bot, channel, sender, args):
    unignore(bot, sender, args)


def unignore(bot, sender, args):
    if sender == bot.config['System']['owner'] and args:
        bot.ignored_users.remove(args[0])
