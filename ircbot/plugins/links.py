import requests
import requests.exceptions
import rfc3987
from bs4 import BeautifulSoup
from ircbot import bot


def allowed_to_process(bot, channel):
    mode = bot.config['Links']['mode']

    if mode == "all":
        return True

    if mode == "whitelist" and channel in bot.config['Links']['channels']:
        return True
    elif mode == "whitelist":
        return False

    if mode == "blacklist" and channel in bot.config['Links']['channels']:
        return False

    return True


def truncate_title(title):
    title = title.replace("\n", "")
    max_length = int(bot.config['Links']['max_length'])
    if len(title) > max_length:
        return "{}...".format(title[:max_length])
    else:
        return title


@bot.hook()
def link_title_parse_hook(bot, channel, sender, message):
    if not allowed_to_process(bot, channel):
        return

    for word in message.split(" "):
        try:
            if rfc3987.match(word, rule='URI'):
                r = requests.get(word)

                if r.status_code != 200:
                    return

                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.head.title.text.strip()
                title = truncate_title(title)

                if title:
                    bot.message(channel, "🔗 {}".format(title))
        except requests.exceptions.InvalidSchema:
            pass
