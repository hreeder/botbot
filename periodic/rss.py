import feedparser
from util import Format


class RSSCallback:
    def __init__(self):
        #                    m    s    ms
        self.callback_time = 15 * 60 * 1000
        self.prefix = "%s[RSS]%s" % (Format.GREEN, Format.RESET)

        self.feeds = {}

    def setup(self, bot):
        self.bot = bot
        for feedname in self.bot.config['Feeds']['active'].split():
            data = {
                "url": self.bot.config['Feeds']["{}_url".format(feedname)],
                "target_channels": self.bot.config['Feeds']["{}_channels".format(feedname)].split()
            }

            f = feedparser.parse(data['url'])
            if "etag" in f:
                data['last_etag'] = f.etag
            if "modified" in f:
                data['last_modified'] = f.modified

            self.feeds[feedname] = data

    def callback(self):
        for key, details in self.feeds.items():
            kwargs = {}
            if "last_etag" in details:
                kwargs['etag'] = details['last_etag']

            if "last_modified" in details:
                kwargs['modified'] = details['last_modified']

            f = feedparser.parse(details['url'], **kwargs)
            if f.status != 304:
                # New Entry!
                for channel in details['target_channels']:
                    self.bot.message(channel, "{} {}: {} ({})".format(
                        self.prefix,
                        f.feed.title,
                        f.entries[0].title,
                        f.entries[0].link
                    ))

                if "etag" in f:
                    details['last_etag'] = f.etag
                if "modified" in f:
                    details['last_modified'] = f.modified
