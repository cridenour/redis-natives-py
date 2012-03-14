from redis import Redis
from redis_natives import Set


class RedisWrapper(object):
    method_calls = []

    def __init__(self, redis):
        self._redis = redis

    def __getattr__(self, name):
        self.method_calls.append(name)
        return getattr(self._redis, name)


class RedisNativesTestCase(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.other_key = 'other_key'


class SetTestCase(RedisNativesTestCase):
    def setup_method(self, method):
        super(SetTestCase, self).setup_method(method)
        self.set = Set(self.redis, self.test_key)
        self.other_set = Set(self.redis, self.other_key)


class IntegerSetTestCase(RedisNativesTestCase):
    def setup_method(self, method):
        super(IntegerSetTestCase, self).setup_method(method)
        self.set = Set(self.redis, self.test_key, type=int)
        self.other_set = Set(self.redis, self.other_key, type=int)
