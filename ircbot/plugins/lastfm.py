import pylast

from redis import StrictRedis
from ircbot import bot, Format


def set_np_user(bot, sender, username):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    redis.set("{}lastfm-{}".format(bot.config['System']['redis_prefix'], sender), username)


def get_np_user(bot, sender):
    redis = StrictRedis.from_url(bot.config['System']['redis_url'])
    return redis.get("{}lastfm-{}".format(bot.config['System']['redis_prefix'], sender))


@bot.command('np')
@bot.command('nowplaying')
def np(bot, channel, sender, args):
    """Now Playing - Gets the currently scrobbling track for a given last.fm user. Usage: np thebigredbutton"""
    from_redis = get_np_user(bot, sender)
    if args:
        user = args[0].strip()
        if len(args) > 1 and args[1] == "--save":
            set_np_user(bot, sender, user)
    elif from_redis:
        user = from_redis.decode('utf-8')
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
            bot.message(channel, "[LastFM] {} is currently listening to {fmt.GREEN}{t.title}{fmt.RESET} by {fmt.ORANGE}{t.artist}{fmt.RESET}".format(user.get_name(), fmt=Format, t=np))
        else:
            last_played = user.get_recent_tracks(limit=2)
            last_played = last_played[0]
            bot.message(channel, "[LastFM] {} is not currently scrobbling - "
                                 "They last listened to {}".format(user.get_name(), last_played.track))
    except pylast.WSError:
            bot.message(channel, "[LastFM] I cannot find the user '{}'".format(user))
