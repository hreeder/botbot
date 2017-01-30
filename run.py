import logging
logging.basicConfig(level=logging.DEBUG)

from ircbot import bot


if __name__ == "__main__":
    bot.load_config("config.ini")
    bot.load_plugins()

    bot._reset_attributes()
    bot._reset_connection_attributes()

    if bot.config['System'].getboolean('debug'):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    bot.connect(bot.config['IRC']['host'], int(bot.config['IRC']['port']), tls=bot.config.getboolean('IRC', 'tls'))
    bot.handle_forever()
