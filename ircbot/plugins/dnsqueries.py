import dns.resolver
import dns.reversename
import ipaddress

from ircbot import bot

@bot.command('host')
def host(bot, channel, sender, args):
    """Query DNS for a hostname. Usage: $host [MX] example.com"""
    if len(args) == 1:
        target = args[0]
        query_types = ["A", "AAAA"]

        try:
            target_ipaddr = ipaddress.ip_address(target)
            target = dns.reversename.from_address(target)
            query_types = ["PTR"]
        except ValueError:
            pass
    elif len(args) == 2 and args[0].upper() in ["A", "AAAA", "CNAME", "HINFO", "ISDN", "MX", "NS", "SRV", "TXT", "RP", "SPF", "PTR"]:
        target = args[1]
        query_types = [args[0].upper()]

    for query_type in query_types:
        try:
            query_response = dns.resolver.query(target, query_type)
            truncated = False

            if channel != sender and len(query_response) > 4:
                query_response = query_response[:4]
                truncated = True

            def get_target(rdata):
                print(dir(rdata))
                if query_type in ["A", "AAAA"]:
                    return rdata.address
                elif query_type in ["CNAME"]:
                    return rdata.target
                elif query_type in ["TXT"]:
                    return ", ".join([s.decode('utf-8') for s in rdata.strings])
                else:
                    return rdata

            for rdata in query_response:
                response = get_target(rdata)
                bot.message(channel, "{} ({}): {}".format(target, query_type, response))

            if truncated:
                bot.message(channel, "Response truncated - more than 4 responses")

        except dns.resolver.NXDOMAIN as ex:
            bot.message(channel, "NXDOMAIN ({}): {}".format(query_type, str(ex)))
        except dns.resolver.NoAnswer as ex:
            bot.message(channel, str(ex))
