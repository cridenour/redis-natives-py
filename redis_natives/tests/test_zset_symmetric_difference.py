from redis_natives.tests import IntegerZSetTestCase


class TestIntegerZSet(IntegerZSetTestCase):
    def test_symmetric_difference(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        symdiff = self.zset.symmetric_difference(set([(2, 2.0), (3, 3.0)]))
        assert symdiff == set([(1, 1.0), (3, 3.0)])

    def test_symmetric_difference_accepts_redis_sets(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.other_zset.add(2, 2)
        self.other_zset.add(3, 3)
        assert self.zset.symmetric_difference(self.other_zset) == \
            set([(1, 1.0), (3, 3.0)])

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

    def test_symmetric_difference_update_accepts_redis_sets(self):
        self.zset.add(1, 1)
        self.zset.add(2, 2)
        self.other_zset.add(2, 2)
        self.other_zset.add(3, 3)
        self.zset.symmetric_difference_update(self.other_zset)
        assert self.zset.data == [(1, 1.0), (3, 3.0)]
