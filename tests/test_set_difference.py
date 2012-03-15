from tests import IntegerSetTestCase, SetTestCase


class TestSetDifference(SetTestCase):
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


class TestIntegerSetDifference(IntegerSetTestCase):
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

    def test_difference_update_accepts_redis_sets(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.other_set.add(2)
        self.set.difference_update(self.other_set)
        assert self.set.data == set([1, 3])

    def test_substraction_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set -= set([1, 2])
        assert self.set.data == set([3])
