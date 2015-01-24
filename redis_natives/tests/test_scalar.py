from redis import Redis

from redis_natives import Scalar
from redis_natives.tests import RedisWrapper


class TestStringScalar(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.str = Scalar(self.redis, self.test_key)
        self.redis.flushdb()
        self.redis.method_calls = []

    def test_simple_assign(self):
        self.str.value = '3'
        assert self.redis.get('test_key') == '3'

    def test_length(self):
        assert len(self.str) == 0
        self.str.value = '3'
        assert len(self.str) == 1

    def test_contains(self):
        self.str.value = '123'
        assert '2' in self.str

    def test_append(self):
        self.str += '123'
        assert self.redis.get('test_key') == '123'

    def test_slicing(self):
        self.str.value = '1234567'
        assert self.str[0:0] == ''
        assert self.str[:] == '1234567'
        assert self.str[0:-1] == '123456'
        assert self.str[:-1] == '123456'
        assert self.str[-1:] == '7'


class TestIntegerScalar(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.int = Scalar(self.redis, self.test_key, type=int)
        self.redis.flushdb()
        self.redis.method_calls = []

    def test_simple_assign(self):
        self.int.value = 3
        assert self.int.value == 3

    def test_length(self):
        assert len(self.int) == 0
        self.int.value = '3'
        assert len(self.int) == 1

    def test_append(self):
        self.int.value = 2
        self.int += 3
        assert self.int.value == 5
