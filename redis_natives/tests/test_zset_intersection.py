from redis_natives.tests import IntegerZSetTestCase


class TestIntegerZSet(IntegerZSetTestCase):
    def test_intersection(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        intersection = self.zset.intersection(set([(1, 1.0), (2, 2.0)]))
        assert intersection == set([(1, 2.0), (2, 4.0)])

    def test_intersection_accepts_redis_zsets(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.other_zset.add(2, 1)
        intersection = self.zset.intersection(self.other_zset)
        assert intersection == set([(2, 3.0)])

    def test_and_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        intersection = self.zset & set([(1, 1.0), (2, 2.0)])
        assert intersection == set([(1, 2.0), (2, 4.0)])

    def test_intersection_update(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset.intersection_update(set([(1, 1.0), (2, 2.0)]),
            aggregate='max')
        assert self.zset.data == [(1, 1.0), (2, 2.0)]

    def test_intersection_update_accepts_redis_zsets(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.other_zset.add(2, 1)
        self.zset.intersection_update(self.other_zset,
            aggregate='min')
        assert self.zset.data == [(2, 1.0)]

    def test_and_assignment_operator(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.zset.add(3, 3)
        self.zset.aggregate = 'max'
        self.zset &= set([(1, 1.0), (2, 2.0)])
        assert self.zset.data == [(1, 1.0), (2, 2.0)]
