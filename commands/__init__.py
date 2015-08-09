from . import internals, help, lastfm, whereis

# Commands should all accept the following arguments
# bot, channel, sender_nickname, arguments
commands = {
    "help": help.help,
    "whereis": whereis.whereis,
    "np": lastfm.np
}

# PM Commands should accept the following arguments
# bot, sender_nickname, arguments
pm_commands = {
    "help": help.help_pm,
    "die": internals.die,
    "nick": internals.nick
}