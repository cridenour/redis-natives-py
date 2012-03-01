from redis import Redis

from redis_natives.datatypes import Dict, Set, ZSet


class TestZSet(object):
    def setup_method(self, method):
        self.redis = Redis()
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.zset = ZSet(self.redis, self.test_key)

    def test_length_initially_zero(self):
        assert len(self.zset) == 0

    def test_add_value_increases_length(self):
        self.zset.add(1, 2)
        assert len(self.zset) == 1

    def test_add_saves_values_in_redis(self):
        self.zset.add(1, 2)
        assert self.redis.zrange('test_key', 0, 1) == ['1']

    def test_remove(self):
        self.zset.add(1, 2)

        self.zset.discard(1)
        assert len(self.zset) == 0


class TestSet(object):
    def setup_method(self, method):
        self.redis = Redis()
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.set = Set(self.redis, self.test_key)

    def test_length_initially_zero(self):
        assert len(self.set) == 0

    def test_add_value_increases_length(self):
        self.set.add(1)
        assert len(self.set) == 1

    def test_add_saves_values_in_redis(self):
        self.set.add(1)
        assert self.redis.smembers('test_key') == set(['1'])

    def test_remove(self):
        self.set.add(1)

        self.set.discard(1)
        assert len(self.set) == 0


class TestDict(object):
    def setup_method(self, method):
        self.redis = Redis()
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.dict = Dict(self.redis, self.test_key)

    def test_length_initially_zero(self):
        assert len(self.dict) == 0

    def test_add_value_increases_length(self):
        self.dict['a'] = 'b'
        assert len(self.dict) == 1

    def test_add_saves_values_in_redis(self):
        self.dict['a'] = 'b'
        assert self.redis.hkeys('test_key') == ['a']

    def test_remove(self):
        self.dict['a'] = 'b'

        del self.dict['a']
        assert len(self.dict) == 0

