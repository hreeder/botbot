import logging
import sys

from ircbot import bot
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    cfg = "config.ini"
    if len(sys.argv) > 1:
        cfg = sys.argv[1]
    bot.load_config(cfg)
    bot.load_plugins()

    bot._reset_attributes()
    bot._reset_connection_attributes()

    if bot.config['System'].getboolean('debug'):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    password = None
    if "password" in bot.config['IRC']:
        password = bot.config['IRC']['password']
    bot.connect(bot.config['IRC']['host'], int(bot.config['IRC']['port']), tls=bot.config.getboolean('IRC', 'tls'), password=password)
    bot.handle_forever()
