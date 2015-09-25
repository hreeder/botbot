from slacker import Slacker


def slackwho(bot, channel, sender, args):
    slacker = Slacker(bot.config['Slack']['api_key'])
    users_response = slacker.users.list(presence=True)
    users = [user['name'] for user in users_response.body['members']]
    users.reverse()

    while users:
        outlist = []
        try:
            for n in range(0,10):
                outlist.append(users.pop())
        except IndexError:
            pass
        output = "Slack Users: %s " % ", ".join(outlist)
        bot.message(sender, output)


def slackwhois(bot, channel, sender, args):
    slacker = Slacker(bot.config['Slack']['api_key'])
    if not args:
        bot.message(channel, "%s: Please supply a user to look up" % sender)
        return
    users_response = slacker.users.list(presence=True)
    users = {user['name']: user for user in users_response.body['members']}

    if args[0] not in users:
        bot.message(channel, "%s: %s was not found in the slack team" % (sender, args[0]))
        return

    user = args[0]
    user = users[user]

    name_str = user['name']
    if user['profile']['real_name']:
        name_str += " (%s)" % user['profile']['real_name']

    bot.message(channel, "Slack User: %s, Presence: %s" % (name_str, user['presence']))