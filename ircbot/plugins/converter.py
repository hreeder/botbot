import pint

from ircbot import bot


@bot.command('convert')
def convert(bot, channel, sender, args):
    """ Converts units from one measurement to another. ie: !conv 100 cm inches """
    amount = float(args[0])
    unit_from = args[1]
    unit_to = args[2]

    try:
        ureg = pint.UnitRegistry()
        unit = ureg.Quantity(amount, unit_from)

        to = unit.to(unit_to)

        bot.message(channel, "{} {} || {} {}".format(amount, unit_from, to.magnitude, to.units))
    except pint.errors.UndefinedUnitError as ex:
        bot.message(channel, str(ex))
    except pint.errors.DimensionalityError as ex:
        bot.message(channel, str(ex))
