from tests import SetTestCase, IntegerSetTestCase


class TestSet(SetTestCase):
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


class TestIntegerSet(IntegerSetTestCase):
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

    def test_clear(self):
        self.set.add(1)
        self.set.clear()
        assert len(self.set) == 0

    def test_iterator(self):
        self.set.add(1)
        self.set.add(2)
        assert [i for i in self.set] == [1, 2]

    def test_redis_type(self):
        self.set.add(1)
        assert self.set.redis_type == 'set'

    def test_issuperset(self):
        self.set.add(1)
        self.set.add(2)
        self.other_set.add(2)
        assert self.set.issuperset(self.other_set)
        self.other_set.add(3)
        assert not self.set.issuperset(self.other_set)

    def test_issubset(self):
        self.set.add(1)
        self.other_set.add(2)
        assert not self.set.issubset(self.other_set)
        self.other_set.add(1)
        assert self.set.issubset(self.other_set)

    def test_isdisjoint(self):
        self.set.add(1)
        self.other_set.add(2)
        assert self.set.isdisjoint(self.other_set)
        self.other_set.add(1)
        assert not self.set.isdisjoint(self.other_set)
