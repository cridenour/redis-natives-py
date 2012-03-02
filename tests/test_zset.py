from redis import Redis
from redis_natives.datatypes import Dict, Set, ZSet
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

    def test_pop(self):
        self.set.add(1)

        assert self.set.pop() == '1'
        assert len(self.set) == 0

    def test_contains(self):
        self.set.add(1)
        assert '1' in self.set

    def test_iterator(self):
        self.set.add(1)
        self.set.add(2)
        assert [i for i in self.set] == ['1', '2']

    def test_redis_type(self):
        self.set.add(1)
        assert self.set.redis_type == 'set'


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

    def test_contains(self):
        self.dict['a'] = 'b'
        assert 'a' in self.dict
        assert 'b' not in self.dict

    def test_iterator(self):
        self.dict['a'] = 'b'
        self.dict['b'] = 'c'
        assert [key for key in self.dict] == ['a', 'b']

    def test_items(self):
        self.dict['a'] = 'b'
        self.dict['b'] = 'c'
        assert self.dict.items() == [('a', 'b'), ('b', 'c')]

    def test_values(self):
        self.dict['a'] = 'b'
        self.dict['b'] = 'c'
        assert self.dict.values() == ['b', 'c']

    def test_keys(self):
        self.dict['a'] = 'b'
        self.dict['b'] = 'c'
        assert self.dict.keys() == ['a', 'b']

    def test_redis_type(self):
        self.dict['a'] = 'b'
        assert self.dict.redis_type == 'hash'



