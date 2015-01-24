from redis_natives.tests import IntegerSetTestCase, SetTestCase


class TestSetUnion(SetTestCase):
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


class TestIntegerSetUnion(IntegerSetTestCase):
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

    def test_update_accepts_redis_sets(self):
        self.other_set.add(2)
        self.other_set.add(3)
        self.set.add(1)
        self.set.update(self.other_set)
        assert self.set.data == set([1, 2, 3])

    def test_or_assignment_operator(self):
        self.set.add(1)
        self.set |= set([2, 3])
        assert self.set.data == set([1, 2, 3])
