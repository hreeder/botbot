import feedparser
import logging
import time
from util import Format


logger = logging.getLogger("BotBot-RSS")


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
                "target_channels": self.bot.config['Feeds']["{}_channels".format(feedname)].split(),
                "method": self.bot.config['Feeds']['{}_method'.format(feedname)],
                "checked": time.time(),
            }

            f = feedparser.parse(data['url'])
            if "etag" in f:
                data['last_etag'] = f.etag
            if "modified" in f:
                data['last_modified'] = f.modified

            if data['method'] == "hash":
                seen = set()
                for entry in f.entries:
                    seen.add(entry)

            title = f.feed.title
            try:
                title = self.bot.config['Feeds']['{}_title_override'.format(feedname)]
            except:
                pass

            data['title'] = title

            self.feeds[feedname] = data

    def callback(self):
        for key, details in self.feeds.items():
            etag = None
            modified = None
            logger.debug("Checking Feed: {}. Last Checked: {}.".format(key, details['checked']))

            if "last_etag" in details and details['method'] in ["any", "etag"]:
                etag = details['last_etag']

            if "last_modified" in details and details['method'] in ["any", "modified"]:
                modified = details['last_modified']

            logger.debug("\tETag: {}, Modified: {}".format(etag, modified))

            f = feedparser.parse(details['url'], etag=etag, modified=modified)
            logger.debug("\tStatus: {}".format(f.status))

            new_entry = []
            if f.status != 304 and details['method'] not in ["hash"]:
                for entry in f.entries:
                    if time.mktime(entry.updated_parsed) > details['checked']:
                        logger.debug("\tEntry: {}. New? {} - entry: {}, checked: {}".format(entry.title, time.mktime(entry.updated_parsed) > details['checked'], time.mktime(entry.updated_parsed), details['checked']))
                        new_entry.append(entry)

            if details['method'] in ["hash"]:
                for entry in f.entries:
                    if entry not in details['seen']:
                        new_entry.append(entry)
                        details['seen'].add(entry)

            if f.status != 304 and new_entry:
                if "etag" in f:
                    logger.debug("\tOld Etag: {}".format(etag))
                    logger.debug("\tNew Etag: {}".format(f.etag))

                if "modified" in f:
                    logger.debug("\tOld Modified: {}".format(modified))
                    logger.debug("\tNew Modified: {}".format(f.modified))

                # New Entr[y|ies]
                for entry in new_entry:
                    for channel in details['target_channels']:
                        self.bot.message(channel, "{} {}: {} ({})".format(
                            self.prefix,
                            details['title'],
                            entry.title,
                            entry.link
                        ))

                # store the updated etag / modified
                if "etag" in f:
                    self.feeds[key]['last_etag'] = f.etag
                if "modified" in f:
                    self.feeds[key]['last_modified'] = f.modified

            self.feeds[key]['checked'] = time.time()
