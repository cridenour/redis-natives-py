from redis import Redis
from redis_natives import ZSet
from tests import RedisWrapper


class TestZSet(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.zset = ZSet(self.redis, self.test_key)
        self.redis.flushdb()
        self.redis.method_calls = []

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

    def test_pop(self):
        self.zset.add(1, 2)

        assert self.zset.pop() == '1'
        assert len(self.zset) == 0

    def test_contains(self):
        self.zset.add(1, 2)
        assert '1' in self.zset
        assert '2' not in self.zset

    def test_iterator(self):
        self.zset.add(1, 2)
        self.zset.add(2, 2)
        assert [i for i in self.zset] == [('1', 2.0), ('2', 2.0)]

    def test_redis_type(self):
        self.zset.add(1, 2)
        assert self.zset.redis_type == 'zset'

    def test_type(self):
        self.zset.add(1, 2)
        assert self.zset.type == str

    def test_integer_type_conversion(self):
        self.zset.type = int
        self.zset.add(1, 2)

        assert self.zset.pop() == 1


class TestIntegerZSet(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.zset = ZSet(self.redis, self.test_key)
        self.redis.flushdb()
        self.redis.method_calls = []

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

    def test_pop(self):
        self.zset.add(1, 2)

        assert self.zset.pop() == '1'
        assert len(self.zset) == 0

    def test_contains(self):
        self.zset.add(1, 2)
        assert '1' in self.zset
        assert '2' not in self.zset

    def test_iterator(self):
        self.zset.add(1, 2)
        self.zset.add(2, 2)
        assert [i for i in self.zset] == [('1', 2.0), ('2', 2.0)]

    def test_redis_type(self):
        self.zset.add(1, 2)
        assert self.zset.redis_type == 'zset'

    def test_type(self):
        self.zset.add(1, 2)
        assert self.zset.type == str

    def test_integer_type_conversion(self):
        self.zset.type = int
        self.zset.add(1, 2)

        assert self.zset.pop() == 1
