import requests
import requests.exceptions
import rfc3987
from bs4 import BeautifulSoup
from ircbot import bot


@bot.hook()
def link_title_parse_hook(bot, channel, sender, message):
    for word in message.split(" "):
        try:
            if rfc3987.match(word, rule='URI'):
                r = requests.get(word)
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.head.title.text.strip()
                title = title.replace("\n", "")
                bot.message(channel, " :: {}".format(title))
        except requests.exceptions.InvalidSchema:
            pass
