import logging
import pydle
import os

from configparser import ConfigParser
from functools import partial
from pluginbase import PluginBase
from pydle.async import EventLoop
from tornado.ioloop import PeriodicCallback

from ircbot.webserver import setup_webserver

logger = logging.getLogger(__name__)

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

plugin_base = PluginBase(package='ircbot.plugins')


class BotBot(pydle.Client):
    def __init__(self, fallback_nicknames=[], username=None, realname=None, **kwargs):
        super(BotBot, self).__init__("botbot-defaultnickname",
                                     fallback_nicknames=fallback_nicknames,
                                     username=username,
                                     realname=realname,
                                     **kwargs)
        self.config = None
        self.join_channels = None
        self.trigger = None
        self.config_location = None
        self.plugin_mgr = None
        self.commands = {}
        self.channel_hooks = []
        self.periodic_tasks = []
        self.ignored_users = set()

        self.event_loop = EventLoop()
        self.webapp, self.webserver = setup_webserver(self)
        self.webapp._ctx = self
        self.webserver_listening = False

    def cleanup(self):
        self.commands = {}
        self.plugins = {}
        self.channel_hooks = []

        for task in self.periodic_tasks:
            task.stop()
        self.periodic_tasks = []

        if self.webapp:
            self.webapp.handlers = []

    def load_config(self, location=None):
        if location:
            self.config_location = location

        self.config = ConfigParser()
        logger.debug(self.config_location)
        if self.config_location:
            self.config.read(self.config_location)
            logger.debug(self.config)

            self._nicknames = [self.config['IRC']['nick']]
            self.nickname = self.config['IRC']['nick']
            logger.debug("Setting Nickname: {}, All: {}".format(self.nickname, self._nicknames))

            if "username" in self.config['IRC']:
                self.username = self.config['IRC']['username']
            else:
                self.username = self.nickname.lower()

            self.trigger = self.config['IRC']['trigger']
            self.join_channels = self.config['IRC']['channel'].split()
            try:
                if not self.webserver_listening:
                    self.webserver = self.webapp.listen(self.config['Webhooks']['port'], self.config['Webhooks']['host'])
                    self.webserver_listening = True
            except:
                pass

    def load_plugins(self):
        self.load_config()
        self.cleanup()
        if self.plugin_mgr:
            self.plugin_mgr.cleanup()

        locations = [get_path('plugins')]
        for location in self.config['System']['plugin_dirs'].split(" "):
            if location:
                locations.append(location)

        self.plugin_mgr = plugin_base.make_plugin_source(
            searchpath=locations
        )

        for plugin_name in self.plugin_mgr.list_plugins():
            if plugin_name in self.config['System']['plugin_blacklist']:
                logger.debug("Ignoring Plugin: {}".format(plugin_name))
                continue

            try:
                plugin_module = self.plugin_mgr.load_plugin(plugin_name)
                logger.debug("Loaded Plugin: {}".format(plugin_name))
                self.plugins[plugin_name] = plugin_module
            except ImportError as ex:
                logger.debug("Unable to load plugin {} - {}".format(plugin_name, ex))
                continue

        [task.setup(self) for task in self.periodic_tasks]
        self.periodic_tasks = [PeriodicCallback(task.callback, task.callback_time, io_loop=self.event_loop.io_loop) for task in self.periodic_tasks]
        [task.start() for task in self.periodic_tasks]

    def command(self, keyword):
        def decorator(f):
            self.register_command(keyword, f)
            return f
        return decorator

    def hook(self, hook_type='channel'):
        def decorator(f):
            if hook_type == 'channel':
                self.register_hook(f)
            return f
        return decorator

    def webhook(self, path):
        def decorator(cls):
            logger.debug("Registering webapp handler {} at {}".format(cls, path))
            self.webapp.add_handlers(r".*", [(path, cls)])
            return cls
        return decorator

    def periodic(self):
        def decorator(cls):
            self.register_periodic(cls)
            return cls
        return decorator

    def register_command(self, command, action):
        logger.debug("Registering Command: {}, {}".format(command, action))
        self.commands[command] = action

    def register_hook(self, channel_hook):
        self.channel_hooks.append(channel_hook)

    def register_periodic(self, clazz):
        logger.debug("Registering periodic callback: {}".format(clazz))
        self.periodic_tasks.append(clazz())

    def on_connect(self):
        for channel in self.join_channels:
            self.join(channel)

    def on_channel_message(self, channel, sender, message):
        if message.startswith(self.trigger):
            message_trigger_removed = message[len(self.trigger):]
            command = message_trigger_removed.split()[0]
            args = message_trigger_removed.split()[1:]

            logger.debug("Command: " + command)
            logger.debug("Args: " + str(args))

            if command in self.commands.keys() and sender not in self.ignored_users:
                logger.debug("Dispatching {} Command".format(command))
                self.commands[command](self, channel, sender, args)
                return

        for chan_hook in self.channel_hooks:
            chan_hook(self, channel, sender, message)

    def on_private_message(self, sender, message):
        if message.startswith(self.trigger):
            message = message[len(self.trigger):]
        command = message.split()[0]
        args = message.split()[1:]

        if command in self.commands.keys():
            self.commands[command](self, sender, sender, args)
            return

    def message(self, channel, msg):
        if msg.count("\n") > int(self.config["IRC"]["maxlines"]) or len(msg) > int(self.config["IRC"]["maxlen"]):
            msg = "\n".join(msg.split("\n")[:int(self.config["IRC"]["maxlines"])])
            msg = msg[:int(self.config["IRC"]["maxlen"])]
            msg += " [...]"

        super().message(channel, msg)
