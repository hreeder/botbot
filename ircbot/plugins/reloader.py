from ircbot import bot


@bot.command('reload')
def reload(bot, channel, sender, args):
    """Owner Command: Reload the bot"""
    if sender == bot.config['System']['owner']:
        bot.load_plugins()
        bot.message(channel, "Reloaded 👍")
