from ircbot import bot, Format
from tornado.web import RequestHandler


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
    if sender == bot.config['System']['owner'] and args:
        bot.ignored_users.add(args[0])


@bot.command('unignore')
def unignore(bot, sender, args):
    if sender == bot.config['System']['owner'] and args:
        bot.ignored_users.remove(args[0])


@bot.command('colorsofthewind')
@bot.command('coloursofthewind')
def channel_test_string(bot, channel, sender, args):
    if sender == bot.config['System']['owner']:
        bot.message(channel, Format.TEST_STRING)


@bot.command('reload')
def reload(bot, channel, sender, args):
    """Owner Command: Reload the bot"""
    if sender == bot.config['System']['owner']:
        bot.load_plugins()
        bot.message(channel, "Reloaded 👍")


@bot.webhook(r"/")
class DefaultHandler(RequestHandler):
    def get(self):
        self.write("Online")
