from . import internals, help, lastfm, whereis, slack, time, karma, broadcasts

# Commands should all accept the following arguments
# bot, channel, sender_nickname, arguments
commands = {
    "help": help.help,
    "whereis": whereis.whereis,
    "np": lastfm.np,
    "slackwho": slack.slackwho,
    "slackwhois": slack.slackwhois,
    "about": help.bot_info,
    "time": time.time,
    "karma": karma.karma_command,
    "top5": karma.top_karma,
    "last5": karma.lowest_karma,
    "bc": broadcasts.broadcast,
    "broadcast-topic-create": broadcasts.create_topic,
    "broadcast-topic-destroy": broadcasts.destroy_topic,
    "broadcast-topic-allow": broadcasts.allow_sender,
    "broadcast-topic-revoke": broadcasts.disallow_sender,
    "broadcast-topic-transfer": broadcasts.transfer_topic,
    "subscriptions": broadcasts.list_topics,
    "subscribe": broadcasts.subscribe,
    "unsubscribe": broadcasts.unsubscribe
}

# PM Commands should accept the following arguments
# bot, sender_nickname, arguments
pm_commands = {
    "help": help.help_pm,
    "die": internals.die,
    "nick": internals.nick,
    "join": internals.join,
    "part": internals.part,
    "msg": internals.message,
    "slacksetavatar": slack.slacksetavatar
}
