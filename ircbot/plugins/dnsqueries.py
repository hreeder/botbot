import dns.resolver
import dns.reversename
import ipaddress

from ircbot import bot

@bot.command('host')
def host(bot, channel, sender, args):
    print(len(args))
    if len(args) == 1:
        target = args[0]
        query_types = ["A", "AAAA"]

        try:
            target_ipaddr = ipaddress.ip_address(target)
            target = dns.reversename.from_address(target)
            query_types = ["PTR"]
        except ValueError:
            pass
    elif len(args) == 2 and args[0].upper() in ["A", "AAAA", "MX", "SRV"]:
        target = args[1]
        query_types = [args[0].upper()]

    for query_type in query_types:
        try:
            query_response = dns.resolver.query(target, query_type)
            for rdata in query_response[:4]:
                bot.message(channel, "{} ({}): {}".format(target, query_type, rdata))
        except dns.resolver.NXDOMAIN as ex:
            bot.message(channel, "NXDOMAIN ({}): {}".format(query_type, str(ex)))
        except dns.resolver.NoAnswer:
            pass
