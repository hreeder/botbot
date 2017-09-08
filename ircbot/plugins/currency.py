import json

from urllib.request import urlopen

from ircbot import bot


def get_currency(currency_a, currency_b):
    endpoint = "http://api.fixer.io/latest?base={}".format(str(currency_a).upper())

    response = urlopen(endpoint).read().decode("utf-8")
    data = json.loads(response)

    currency_ratio = data["rates"][str(currency_b).upper()]

    return currency_ratio


@bot.command('currency')
def command(bot, channel, sender, args):
    """Converts Currency. Usage: $currency 10 usd gbp"""
    if len(args) < 3:
        bot.message(channel, "This command requires 3 arguments.")
        return
    amount_a = args[0]
    currency_a = str(args[1])
    currency_b = str(args[2])

    currency_ratio = get_currency(currency_a, currency_b)

    amount_b = float(amount_a) * currency_ratio

    bot.message(channel, "{}{} is equal to {}{}".format(str(amount_a), currency_a.upper(), str(round(amount_b, 2)), currency_b.upper()))
