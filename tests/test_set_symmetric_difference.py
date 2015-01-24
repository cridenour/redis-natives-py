from tests import IntegerSetTestCase, SetTestCase


class TestSetDifference(SetTestCase):
    def test_symmetric_difference(self):
        self.set.add(1)
        self.set.add(2)
        sym_diff = self.set.symmetric_difference(set(['2', '3']))
        assert sym_diff == set(['1', '3'])

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


class TestIntegerSetSymmetricDifference(IntegerSetTestCase):
    def test_symmetric_difference(self):
        self.set.add(1)
        self.set.add(2)
        assert self.set.symmetric_difference([2, 3]) == set([1, 3])

    def test_symmetric_difference_accepts_redis_sets(self):
        self.set.add(1)
        self.set.add(2)
        self.other_set.add(2)
        self.other_set.add(3)
        assert self.set.symmetric_difference(self.other_set) == set([1, 3])

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
