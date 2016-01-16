from . import internals, help, lastfm, whereis, slack, time, karma

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
    "last5": karma.lowest_karma
}

# PM Commands should accept the following arguments
# bot, sender_nickname, arguments
pm_commands = {
    "help": help.help_pm,
    "die": internals.die,
    "nick": internals.nick,
    "join": internals.join,
    "part": internals.part,
    "slacksetavatar": slack.slacksetavatar
}