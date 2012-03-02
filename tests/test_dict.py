from redis import Redis
from redis_natives.datatypes import Dict
from tests import RedisWrapper


class TestDict(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
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
