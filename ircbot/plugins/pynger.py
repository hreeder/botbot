import subprocess as sp
import ipaddress
import dns.resolver


from ircbot import bot


@bot.command('ping')
def ipcheck(bot, channel, sender, args):
    """Ping a host. Usage: {bot.trigger}ping example.com"""
    ip = args[0]
    targets = []
    truncated = False

    try:
        targets.append(ipaddress.ip_address(ip))
    except ValueError:
        query_responses = []
        for qtype in ["A", "AAAA"]:
            result = []
            try:
                result = dns.resolver.query(ip, qtype)
            except dns.resolver.NXDOMAIN as ex:
                bot.message(channel, "NXDOMAIN ({}): {}".format(qtype, str(ex)))
            except dns.resolver.NoAnswer as ex:
                pass
            if channel != sender and len(result) > 4:
                result = result[:4]
                truncated = True
            query_responses.extend(result)
        targets = [ipaddress.ip_address(rdata.address) for rdata in query_responses]

    for address in targets:
        if isinstance(address, ipaddress.IPv4Address):
            binary = "ping"
        elif isinstance(address, ipaddress.IPv6Address):
            binary = "ping6"
        else:
            bot.message(channel, "💩")
            return

        status, result = sp.getstatusoutput("{} -c1 -w2 {}".format(binary, str(address)))
        if status == 0:
            bot.message(channel, 'Host {} is Up!'.format(str(address)))
        else:
            bot.message(channel, 'Host {} is Down!'.format(str(address)))

    if truncated:
        bot.message(channel, "Response truncated - DNS Lookup contained more than 4 records (A / AAAA treated independently)")
