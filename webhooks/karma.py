from redis import StrictRedis
from tornado.web import RequestHandler


class KarmaHandler(RequestHandler):
    def get(self):
        bot = self.application._ctx
        redis = StrictRedis.from_url(bot.config['System']['redis_url'])
        all_karma = redis.hgetall(bot.config['System']['redis_prefix'] + "karma")
        all_karma = {k.decode('utf-8'): int(v) for k, v in all_karma.items()}
        self.write(all_karma)
