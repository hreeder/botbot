# botbot
Botbot is an irc bot mostly developed for personal entertainment and some various utility functions.

## Setup
Botbot is developed in Python 3, so please ensure that is installed on your system prior to following these steps.

1. Ensure you have [Pipenv](https://pipenv.readthedocs.io/en/latest/) installed.

2. Install Requirements with `pipenv install`. Install development dependencies with `pipenv install --dev`.

3. Create a configuration. Copy the distributable file from `config.ini.dist` to `config.ini` and edit as necessary.

## config.ini
config.ini grows along with botbot. It is divided into sections as required.
### IRC
* host - Your irc server, ie `chat.freenode.net`
* port - Port to connect on, will often be 6697 (if using TLS) or 6667 (if not)
* channel - Space separated list of channels to join on connect, ie `#botbot #botchanneltwo`
* nick - Nickname for the bot to use
* tls - `True` or `False`, connect to the network securely
* trigger - What character must lines start with for the bot to attempt looking up a command

### Webhooks
* host - What interface should the webhooks server listen on
* port - What port should the webhooks server listen on

### system
* debug - Sets logging level
* die_password - set a unique password to pass to the bot when issuing the `die` command
* owner - The bot owner's irc nickname.
* repo - Where this instance of the bot's code lives, so people know where they can submit issues
* redis_url - Connection string for redis
* redis_prefix - Prefix to use on any redis keys
* command_blacklist - Space separated list of any commands to ignore while loading commands on bot startup.
* pm_command_blacklist - Same as above, except for PMs
* hook_blacklist - Space separated list of hooks to ignore while loading channel hooks

### Slack
* listen - Space separated list of channels to listen for forwarding to Slack
* api_key - Slack API Key
* webhook - Incoming webhook URL for Slack
* <channel>_target - replace `<channel>` with the channel you are listening to, and set the value to the slack channel to output to (ie `mychannel_target = #general`)

### LastFM
Key and Secret from your Last.FM account

### Yandex
Get an API key from https://tech.yandex.com/translate/

### OpenWeatherMap
Get an API key from http://openweathermap.org/appid#get


## Running Botbot
To run botbot, run `botbot.py`. The script will take an argument of the location to a configuration file optionally, however by default it will attempt to use `config.ini`
