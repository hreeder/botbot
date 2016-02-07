import commands
import hooks
import logging
import pydle
import sys

from configparser import ConfigParser

logger = logging.getLogger("BotBot-Bot")


class BotBot(pydle.Client):
    def __init__(self, config, fallback_nicknames=[], username=None, realname=None, **kwargs):
        super(BotBot, self).__init__(config['IRC']['nick'],
                                     fallback_nicknames=fallback_nicknames,
                                     username=username,
                                     realname=realname,
                                     **kwargs)
        self.join_channels = config['IRC']['channel'].split()
        self.trigger = config['IRC']['trigger']
        self.config = config
        self.commands = {}
        self.pm_commands = {}
        self.channel_hooks = []

    def register_command(self, command, action, type="channel"):
        if type == "pm":
            self.pm_commands[command] = action
        else:
            self.commands[command] = action

    def register_hook(self, channel_hook):
        self.channel_hooks.append(channel_hook)

    def on_connect(self):
        for channel in self.join_channels:
            self.join(channel)

    def on_channel_message(self, channel, sender, message):
        if message.startswith(self.trigger):
            message = message[len(self.trigger):]
            command = message.split()[0]
            args = message.split()[1:]

            logger.debug("Command: " + command)
            logger.debug("Args: " + str(args))

            if command in self.commands.keys():
                self.commands[command](self, channel, sender, args)
                return

        for chan_hook in self.channel_hooks:
            chan_hook(self, channel, sender, message)

    def on_private_message(self, sender, message):
        command = message.split()[0]
        args = message.split()[1:]

        if command in self.pm_commands.keys():
            self.pm_commands[command](self, sender, args)


if __name__ == "__main__":
    config = ConfigParser()

    # Attempt to read the specified config file, else read a default config.ini
    try:
        config.read(sys.argv[1])
    except IndexError:
        config.read("config.ini")

    if config['System'].getboolean('debug'):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    client = BotBot(config)

    for command in commands.commands:
        if command not in config['System']['command_blacklist'].split(" "):
            client.register_command(command, commands.commands[command])

    for command in commands.pm_commands:
        if command not in config['System']['pm_command_blacklist'].split(" "):
            client.register_command(command, commands.pm_commands[command], type="pm")

    for hook in hooks.hooks:
        if hook.__module__.split(".")[1] not in config['System']['hook_blacklist'].split(" "):
            client.register_hook(hook)

    client.connect(config['IRC']['host'], int(config['IRC']['port']))
    client.handle_forever()
    
