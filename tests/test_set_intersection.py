from tests import IntegerSetTestCase, SetTestCase


class TestSetIntersection(SetTestCase):
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

    def test_intersection_update_with_multiple_args(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set.add(4)
        self.other_set.add(2)
        self.other_set.add(3)
        self.set.intersection_update(set(['2', '3', '4']), self.other_set)
        assert self.set.data == set(['2', '3'])

    def test_and_assignment_operator(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.set &= set(['1', '2'])
        assert self.set.data == set(['1', '2'])


class TestIntegerSetIntersection(IntegerSetTestCase):
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
