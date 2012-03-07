from pytest import raises
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


class TestZSetSlicing(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.zset = ZSet(self.redis, self.test_key)
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


class TestIntegerZSet(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.test_key = 'test_key'
        self.zset = ZSet(self.redis, self.test_key, type=int)
        self.redis.flushdb()
        self.redis.method_calls = []

    def test_length_initially_zero(self):
        assert len(self.zset) == 0

    def test_add_value_increases_length(self):
        self.zset.add(1, 2)
        assert len(self.zset) == 1

    def test_add_saves_values_in_redis(self):
        self.zset.add(1, 2)
        assert self.zset[0] == (1, 2.0)

    def test_remove(self):
        self.zset.add(1, 2)
        self.zset.discard(1)
        assert len(self.zset) == 0

    def test_pop(self):
        self.zset.add(1, 2)
        assert self.zset.pop() == 1
        assert len(self.zset) == 0

    def test_contains(self):
        self.zset.add(1, 2)
        assert 1 in self.zset
        assert 2 not in self.zset

    def test_iterator(self):
        self.zset.add(1, 2)
        self.zset.add(2, 2)
        assert [i for i in self.zset] == [(1, 2.0), (2, 2.0)]

    def test_type(self):
        self.zset.add(1, 2)
        assert self.zset.type == int

    def test_integer_type_conversion(self):
        self.zset.add(1, 2)
        assert self.zset.pop() == 1

    def test_intersection(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        intersection = self.zset.intersection(set([(1, 1.0), (2, 2.0)]))
        assert intersection == set([(1, 1.0), (2, 2.0)])

    def test_and_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        intersection = self.zset & set([(1, 1.0), (2, 2.0)])
        assert intersection == set([(1, 1.0), (2, 2.0)])

    def test_intersection_update(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset.intersection_update(set([(1, 1.0), (2, 2.0)]))
        assert self.zset.data == [(1, 1.0), (2, 2.0)]

    def test_and_assignment_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset &= set([(1, 1.0), (2, 2.0)])
        assert self.zset.data == [(1, 1.0), (2, 2.0)]

    def test_symmetric_difference(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        symdiff = self.zset.symmetric_difference(set([(2, 2.0), (3, 3.0)]))
        assert symdiff == set([(1, 1.0), (3, 3.0)])

    def test_xor_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        symdiff = self.zset ^ set([(2, 2.0), (3, 3.0)]) ^ set([(4, 4.0)])
        assert symdiff == set([(1, 1.0), (3, 3.0), (4, 4.0)])

    def test_symmetric_difference_update(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.symmetric_difference_update(set([(2, 2.0), (3, 3.0)]))
        assert self.zset.data == [(1, 1.0), (3, 3.0)]

    def test_xor_assignment_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset ^= set([(2, 2.0), (3, 3.0)])
        assert self.zset.data == [(1, 1.0), (3, 3.0)]

    def test_difference(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        diff = self.zset.difference(set([(1, 1.0), (2, 2.0)]))
        assert diff == set([(3, 3.0)])

    def test_substraction_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        assert self.zset - set([(1, 1.0), (2, 2.0)]) == set([(3, 3.0)])

    def test_difference_update(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset.difference_update(set([(1, 1.0), (2, 2.0)]))
        assert self.zset.data == [(3, 3.0)]

    def test_substraction_assignment_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset -= set([(1, 1.0), (2, 2.0)])
        assert self.zset.data == [(3, 3.0)]

    def test_union(self):
        self.zset.add(1, 1)
        union = self.zset.union([(2, 2.0), (3, 3.0)])
        assert union == set([(1, 1.0), (2, 2.0), (3, 3.0)])

    def test_or_operator(self):
        self.zset.add(1, 1)
        union = self.zset | set([(2, 2.0), (3, 3.0)])
        assert union == set([(1, 1.0), (2, 2.0), (3, 3.0)])

    def test_update(self):
        self.zset.add(1, 1)
        self.zset.update(set([(2, 2.0), (3, 3.0)]))
        assert self.zset.data == [(1, 1.0), (2, 2.0), (3, 3.0)]

    def test_or_assignment_operator(self):
        self.zset.add(1, 1)
        self.zset |= set([(2, 2.0), (3, 3.0)])
        assert self.zset.data == [(1, 1.0), (2, 2.0), (3, 3.0)]
