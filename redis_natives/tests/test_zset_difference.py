from redis_natives.tests import IntegerZSetTestCase


class TestIntegerZSet(IntegerZSetTestCase):
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

    # def test_difference_accepts_redis_sets(self):
    #     self.zset.add(1, 1)
    #     self.zset.add(2, 2)
    #     self.zset.add(3, 3)
    #     self.other_zset.add(2, 3)
    #     self.other_zset.add(3, 1)
    #     diff = self.zset.difference(self.other_zset)
    #     assert diff == set([(1, 1.0)])

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
