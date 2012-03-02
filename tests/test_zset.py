from redis import Redis

from redis_natives.datatypes import Dict, List, Set, ZSet


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

    def test_pop(self):
        self.zset.add(1, 2)

        assert self.zset.pop() == '1'
        assert len(self.zset) == 0

    def test_contains(self):
        self.zset.add(1, 2)
        assert '1' in self.zset
        assert '2' not in self.zset


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


class TestList(object):
    def setup_method(self, method):
        self.redis = Redis()
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.list = List(self.redis, self.test_key)

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


class TestListGetItem(object):
    def setup_method(self, method):
        self.redis = Redis()
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
