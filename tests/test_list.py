from redis import Redis
from redis_natives.datatypes import List
from tests import RedisWrapper


class TestList(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.list = List(self.redis, self.test_key)
        self.redis.flushdb()
        self.redis.method_calls = []

    def test_length_initially_zero(self):
        assert len(self.list) == 0

    def test_append_value_increases_length(self):
        self.list.append(1)
        assert len(self.list) == 1

    def test_append_saves_values_in_redis(self):
        self.list.append(1)
        assert self.redis.lrange('test_key', 0, 1) == ['1']

    def test_remove(self):
        self.list.append(1)

        self.list.remove(1)
        assert len(self.list) == 0

    def test_contains(self):
        self.list.append(1)
        assert '1' in self.list
        assert '2' not in self.list

    def test_iterator(self):
        self.list.append(1)
        self.list.append(2)
        assert [i for i in self.list] == ['1', '2']

    def test_insert(self):
        self.list.append(1)
        self.list.insert(0, 2)

        assert [i for i in self.list] == ['2', '1']

    def test_pop(self):
        self.list.append(1)
        assert self.list.pop() == '1'

    def test_popping_first_item_uses_lpop(self):
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.redis.method_calls = []
        assert self.list.pop(0) == '1'
        assert self.redis.method_calls == ['lpop']

    def test_redis_type(self):
        self.list.append(1)
        assert self.list.redis_type == 'list'


class TestListGetItem(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.list = List(self.redis, self.test_key)
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.list.append(4)

    def test_length_returns_list_length(self):
        assert len(self.list) == 4

    def test_get_list_item_by_range(self):
        assert self.list[0:-1] == ['1', '2', '3', '4']

    def test_get_list_item(self):
        assert self.list[1] == '2'

    def test_set_list_item(self):
        self.list[2] = 123
        assert self.list[2] == '123'

    def test_set_items_by_range(self):
        self.list[1:2] = 5
        assert self.list[1] == '5'
        assert self.list[2] == '5'

    def test_pop(self):
        self.list.pop() == '4'


class TestIntegerList(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.list = List(self.redis, self.test_key, type=int)
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.list.append(4)
        self.redis.method_calls = []

    def test_length_returns_list_length(self):
        assert len(self.list) == 4

    def test_get_list_item_by_range(self):
        assert self.list[0:-1] == [1, 2, 3, 4]

    def test_get_list_item(self):
        assert self.list[1] == 2

    def test_set_list_item(self):
        self.list[2] = 123
        assert self.list[2] == 123

    def test_set_items_by_range(self):
        self.list[1:2] = 5
        assert self.list[1] == 5
        assert self.list[2] == 5

    def test_pop(self):
        self.list.pop() == 4

    def test_remove(self):
        self.list.remove(1)
        assert len(self.list) == 3

    def test_contains(self):
        assert 1 in self.list
        assert 5 not in self.list

    def test_iterator(self):
        assert [i for i in self.list] == [1, 2, 3, 4]

    def test_insert(self):
        self.list.insert(0, 2)

        assert [i for i in self.list] == [2, 1, 2, 3, 4]

    def test_popping_first_item_uses_lpop(self):
        self.redis.method_calls = []
        assert self.list.pop(0) == 1
        assert self.redis.method_calls == ['lpop']
