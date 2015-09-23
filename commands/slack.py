from slacker import Slacker


def slackwho(bot, channel, sender, args):
    slacker = Slacker(bot.config['Slack']['api_key'])
    users_response = slacker.users.list(presence=True)
    for user in users_response.body['members']:
        output = "Slack: %s " % user['name']
        if user['real_name']:
            output += "(%s) " % user['real_name']
        output += "Presence: " + user['presence']
        bot.message(sender, output)
