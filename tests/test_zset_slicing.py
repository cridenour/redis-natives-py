from pytest import raises
from tests import ZSetTestCase


class TestZSetSlicing(ZSetTestCase):
    def setup_method(self, method):
        super(TestZSetSlicing, self).setup_method(method)
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset.add(4, 4)

    def test_get_list_item_by_range(self):
        assert self.zset[0:-1] == [('1', 1.0), ('2', 2.0), ('3', 3.0)]

    def test_get_list_item_by_range_with_open_end(self):
        assert self.zset[0:] == [
            ('1', 1.0),
            ('2', 2.0),
            ('3', 3.0),
            ('4', 4.0)
        ]

    def test_get_list_item_by_range_with_open_start(self):
        assert self.zset[:2] == [('1', 1.0), ('2', 2.0)]

    def test_get_list_item_by_range_with_open_start_and_end(self):
        assert self.zset[:] == [
            ('1', 1.0),
            ('2', 2.0),
            ('3', 3.0),
            ('4', 4.0)
        ]

    def test_get_list_item(self):
        assert self.zset[1] == ('2', 2.0)

    def test_get_list_item_with_negative_inde(self):
        assert self.zset[-1] == ('4', 4.0)

    def test_set_list_item(self):
        self.zset[2] = 123
        assert self.zset[2] == ('123', 3.0)

    def test_set_items_by_range_throws_exception(self):
        with raises(TypeError):
            self.zset[1:2] = 5

    def test_pop(self):
        self.zset.pop() == '4'
