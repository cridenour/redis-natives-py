from redis import Redis
from redis_natives import Set
from tests import RedisWrapper


class TestSet(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
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

    def test_intersection(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        assert self.set.intersection(set(['1', '2'])) == set(['1', '2'])

    def test_and_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        assert self.set & set(['1', '2']) == set(['1', '2'])

    def test_intersection_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.intersection_update(set(['1', '2']))
        assert self.set.data == set(['1', '2'])

    def test_and_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set &= set(['1', '2'])
        assert self.set.data == set(['1', '2'])

    def test_symmetric_difference(self):
        self.set.add(1)
        self.set.add(2)
        assert self.set.symmetric_difference(['2', '3']) == set(['1', '3'])

    def test_xor_operator(self):
        self.set.add(1)
        self.set.add(2)
        assert self.set ^ set(['2', '3']) ^ set(['4']) == set(['1', '3', '4'])

    def test_symmetric_difference_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.symmetric_difference_update(['2', '3'])
        assert self.set.data == set(['1', '3'])

    def test_xor_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set ^= set(['2', '3'])
        assert self.set.data == set(['1', '3'])

    def test_difference(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        assert self.set.difference(set(['1', '2'])) == set(['3'])

    def test_substraction_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        assert self.set - set(['1', '2']) == set(['3'])

    def test_difference_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.difference_update(set(['1', '2']))
        assert self.set.data == set(['3'])

    def test_substraction_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set -= set(['1', '2'])
        assert self.set.data == set(['3'])

    def test_union(self):
        self.set.add(1)
        self.set = self.set.union(['2', '3'])
        assert self.set == set(['1', '2', '3'])

    def test_or_operator(self):
        self.set.add(1)
        assert self.set | set(['2', '3']) == set(['1', '2', '3'])

    def test_update(self):
        self.set.add(1)
        self.set.update(['2', '3'])
        assert self.set.data == set(['1', '2', '3'])

    def test_or_assignment_operator(self):
        self.set.add(1)
        self.set |= set(['2', '3'])
        assert self.set.data == set(['1', '2', '3'])

    def test_add_operator(self):
        self.set.add(3)

        assert self.set | set(['1', '2']) == set(['1', '2', '3'])


class TestIntegerSet(object):
    def setup_method(self, method):
        self.redis = RedisWrapper(Redis())
        self.redis.flushdb()
        self.test_key = 'test_key'
        self.other_key = 'other_key'
        self.set = Set(self.redis, self.test_key, type=int)
        self.other_set = Set(self.redis, self.other_key, type=int)

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
        assert self.set.pop() == 1
        assert len(self.set) == 0

    def test_contains(self):
        self.set.add(1)
        assert 1 in self.set

    def test_iterator(self):
        self.set.add(1)
        self.set.add(2)
        assert [i for i in self.set] == [1, 2]

    def test_redis_type(self):
        self.set.add(1)
        assert self.set.redis_type == 'set'

    def test_intersection(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        assert self.set.intersection(set([1, 2])) == set([1, 2])

    def test_and_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        assert self.set & set([1, 2]) == set([1, 2])

    def test_intersection_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.intersection_update(set([1, 2]))
        assert self.set.data == set([1, 2])

    def test_intersection_update_with_multiple_args(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.add(4)
        self.other_set.add(2)
        self.other_set.add(3)
        self.set.intersection_update(set([2, 3, 4]), self.other_set)
        assert self.set.data == set([2, 3])

    def test_and_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set &= set([1, 2])
        assert self.set.data == set([1, 2])

    def test_symmetric_difference(self):
        self.set.add(1)
        self.set.add(2)
        assert self.set.symmetric_difference([2, 3]) == set([1, 3])

    def test_xor_operator(self):
        self.set.add(1)
        self.set.add(2)
        assert self.set ^ set([2, 3]) ^ set([4]) == set([1, 3, 4])

    def test_symmetric_difference_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.symmetric_difference_update([2, 3])
        assert self.set.data == set([1, 3])

    def test_xor_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set ^= set([2, 3])
        assert self.set.data == set([1, 3])

    def test_difference(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        assert self.set.difference(set([1, 2])) == set([3])

    def test_substraction_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        assert self.set - set([1, 2]) == set([3])

    def test_difference_update(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.difference_update(set([1, 2]))
        assert self.set.data == set([3])

    def test_substraction_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set -= set([1, 2])
        assert self.set.data == set([3])

    def test_union(self):
        self.set.add(1)
        self.set = self.set.union([2, 3])
        assert self.set == set([1, 2, 3])

    def test_or_operator(self):
        self.set.add(1)
        assert self.set | set([2, 3]) == set([1, 2, 3])

    def test_update(self):
        self.set.add(1)
        self.set.update([2, 3])
        assert self.set.data == set([1, 2, 3])

    def test_update_with_another_redis_set(self):
        otherset = Set(self.redis, 'other_key')
        otherset.add(2)
        otherset.add(3)

        self.set.add(1)
        self.set.update(otherset)
        assert self.set.data == set([1, 2, 3])

    def test_or_assignment_operator(self):
        self.set.add(1)
        self.set |= set([2, 3])
        assert self.set.data == set([1, 2, 3])

    def test_add_operator(self):
        self.set.add(3)
        assert self.set | set([1, 2]) == set([1, 2, 3])
