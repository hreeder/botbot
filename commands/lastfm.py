import pylast


def np(bot, channel, sender, args):
    """Now Playing - Gets the currently scrobbling track for a given last.fm user. Usage: np thebigredbutton"""
    if args:
        user = args[0].strip()
    else:
        user = sender
    network = pylast.LastFMNetwork(
        api_key=bot.config['LastFM']['key'],
        api_secret=bot.config['LastFM']['secret']
    )

    try:
        user = network.get_user(user)
        np = user.get_now_playing()
        if np:
            bot.message(channel, "[LastFM] %s is currently listening to '%s'" % (user.get_name(), np))
        else:
            bot.message(channel, "[LastFM] %s is not currently scrobbling" % user.get_name())
    except pylast.WSError:
            bot.message(channel, "[LastFM] I cannot find the user '%s'" % user)