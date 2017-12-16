from ircbot import bot, Format
from tornado.web import RequestHandler


@bot.command('gitrekt')
def crash(bot, channel, sender, args):
    """Owner Command: Testing Sentry"""
    if sender == bot.config['System']['owner']:
        raise NotImplementedError()


@bot.command('die')
def die(bot, channel, sender, args):
    """Owner Command: Causes the bot to disconnect"""
    if sender == bot.config['System']['owner'] and args and args[0] == bot.config['System']['die_password']:
        bot.disconnect()


@bot.command('nick')
def nick(bot, channel, sender, args):
    """Owner Command: Causes the bot to change it's nick"""
    if sender == bot.config['System']['owner'] and args:
        bot.set_nickname(args[0])


@bot.command('join')
def join(bot, channel, sender, args):
    """Owner Command: Causes the bot to join a channel"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        if len(args) > 1:
            # Channel has a password
            bot.join(args[0], password=args[1])
        else:
            bot.join(args[0])


@bot.command('part')
def part(bot, channel, sender, args):
    """Owner Command: Causes the bot to part a channel"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        message = None
        if len(args) > 1:
            message = args[1]
        if bot.in_channel(args[0]):
            bot.part(args[0], message=message)


@bot.command('msg')
def message(bot, channel, sender, args):
    """Owner Command: Sends a message to a channel as the bot"""
    if sender == bot.config['System']['owner'] and args and args[0].startswith("#"):
        message = " ".join(args[1:])
        bot.message(args[0], message)


@bot.command('ignore')
def ignore(bot, channel, sender, args):
    """Owner Command: Ignores a users's messages"""
    if sender == bot.config['System']['owner'] and args:
        print("Ignoring: '{}'".format(args[0]))
        bot.ignored_users.add(args[0])


@bot.command('unignore')
def unignore(bot, channel, sender, args):
    """Owner Command: Starts listening to a users's messages again"""
    if sender == bot.config['System']['owner'] and args:
        print("Unignoring: '{}'".format(args[0]))
        bot.ignored_users.remove(args[0])


@bot.command(['colorsofthewind', 'coloursofthewind'])
def channel_test_string(bot, channel, sender, args):
    """Owner Command: Test string with sweet, rainbow colours. Our pride and joy."""
    if sender == bot.config['System']['owner']:
        bot.message(channel, Format.TEST_STRING)


@bot.webhook(r"/")
class DefaultHandler(RequestHandler):
    def get(self):
        self.write("Online")
