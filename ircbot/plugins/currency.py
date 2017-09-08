import requests

from ircbot import bot


def get_exchange_rate(base_currency: str, target_currency: str):
    endpoint = "http://api.fixer.io/latest"

    resp = requests.get(endpoint, params={"base": base_currency})

    return resp.json()['rates'][target_currency]


@bot.command('currency')
def command(bot, channel, sender, args):
    """Converts Currency. Usage: {bot.trigger}currency 10 usd gbp"""
    if len(args) < 3:
        bot.message(channel, "This command requires 3 arguments, e.g. {}currency 10 usd gbp".format(bot.trigger))
        return
    amount_a = args[0]
    base_currency = args[1].upper()
    target_currency = args[2].upper()

    exchange_rate = get_exchange_rate(base_currency, target_currency)

    amount_b = float(amount_a) * exchange_rate

    bot.message(channel, "{}{} is equal to {}{}".format(
        amount_a,
        base_currency,
        round(amount_b, 2),
        target_currency
    ))
