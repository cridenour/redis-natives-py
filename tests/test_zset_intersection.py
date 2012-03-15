from tests import IntegerZSetTestCase


class TestIntegerZSet(IntegerZSetTestCase):
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
