from redis import Redis
from redis_natives import List
from tests import RedisWrapper


class TestListSlicing(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.list = List(self.redis, self.test_key)
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.list.append(4)

    def test_get_list_item_by_range(self):
        assert self.list[0:-1] == ['1', '2', '3']

    def test_get_list_item_by_range_with_open_end(self):
        assert self.list[0:] == ['1', '2', '3', '4']

    def test_get_list_item_by_range_with_open_start(self):
        assert self.list[:2] == ['1', '2']

    def test_get_list_item_by_range_with_open_start_and_end(self):
        assert self.list[:] == ['1', '2', '3', '4']

    def test_get_list_item(self):
        assert self.list[1] == '2'

    def test_set_list_item(self):
        self.list[2] = 123
        assert self.list[2] == '123'

    def test_set_items_by_range(self):
        self.list[1:2] = 5
        assert self.list[1] == '5'
        assert self.list[2] == '5'

    def test_set_list_item_by_range_with_open_end(self):
        self.list[2:] = '5'
        assert self.list[:] == ['1', '2', '5', '5']

    def test_set_list_item_by_range_with_open_start(self):
        self.list[:2] = '5'
        assert self.list[:2] == ['5', '5']

    def test_set_list_item_by_range_with_open_start_and_end(self):
        self.list[:] = '5'
        assert self.list[:] == ['5', '5', '5', '5']

    def test_pop(self):
        self.list.pop() == '4'
