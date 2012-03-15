from time import time
from .errors import RedisTypeError, RedisKeyError
from .datatypes import RedisSortable, Comparable, SetOperatorMixin


class Set(RedisSortable, Comparable, SetOperatorMixin):
    """
    Re-implements the complete interface of the native ``set`` datatype
    as a bound ``RedisDataType``. Use it exactly as you'd use a ``set``.
    """

    __slots__ = ("_key", "_client", "_pipe")

    def __init__(self, client, key, iter=[], type=str):
        super(Set, self).__init__(client, key, type)
        if hasattr(iter, "__iter__") and len(iter):
            # TODO: What if the key already exists?
            for el in iter:
                self._pipe.sadd(key, el)
            self._pipe.execute()

    def __len__(self):
        return self._client.scard(self.key)

    def __contains__(self, value):
        return self._client.sismember(self.key, self.type_prepare(value))

    def __iter__(self):
        # TODO: Is there a better way than getting ALL at once?
        for el in self.data:
            yield el

    def __repr__(self):
        return str(self._client.smembers(self.key))

    @property
    def data(self):
        return set(map(self.type_convert, self._client.smembers(self.key)))

    def add(self, el):
        """
        Add element ``el`` to this ``Set``
        """
        return self._client.sadd(self.key, self.type_prepare(el))

    def clear(self):
        """
        Purge/delete all elements from this set
        """
        return self._client.delete(self.key)

    def copy(self, key):
        """
        Return copy of this ``Set`` as
        """
        # TODO: Return native set-object instead of bound redis item?
        self._client.sunionstore(key, [self.key])
        return Set(key, self._client)

    def difference(self, *others):
        """
        Return the difference between this set and other as new set
        """
        rset_keys, sets = self._split_by_type(others)
        pipe = self._pipe
        temporary_key = '__temp__'
        if sets:
            rset_keys.append(temporary_key)
            for native_set in sets:
                for element in native_set:
                    pipe.sadd(temporary_key, element)

        if rset_keys:
            rset_keys.insert(0, self.key)
            pipe.sdiff(rset_keys)
        pipe.delete(temporary_key)
        return set(map(self.type_convert, pipe.execute()[-2]))

    def difference_update(self, *others):
        """
        Remove all elements of other sets from this set
        """
        rset_keys, sets = self._split_by_type(others)
        pipe = self._pipe
        temporary_key = '__temp__'
        if sets:
            rset_keys.append(temporary_key)
            for native_set in sets:
                for element in native_set:
                    pipe.sadd(temporary_key, element)

        if rset_keys:
            rset_keys.insert(0, self.key)
            pipe.sdiffstore(self.key, rset_keys)
        pipe.delete(temporary_key)
        pipe.execute()

    # TODO: Implement difference_copy?

    def discard(self, member):
        """
        Remove ``member`` form this set; Do nothing when element is not a member.
        """
        self._client.srem(self.key, self.type_prepare(member))

    def intersection(self, *others):
        """
        Return the intersection of this set and others as new set
        """
        rset_keys, sets = self._split_by_type(others)
        pipe = self._pipe
        temporary_key = '__temp__'
        tmp_keys = []
        if sets:
            for index, native_set in enumerate(sets):
                tmp_key = temporary_key + str(index)
                tmp_keys.append(tmp_key)
                rset_keys.append(tmp_key)
                for element in native_set:
                    pipe.sadd(tmp_key, element)

        if rset_keys:
            rset_keys.insert(0, self.key)
            pipe.sinter(rset_keys)
        for tmp_key in tmp_keys:
            pipe.delete(tmp_key)
        return set(map(self.type_convert, pipe.execute()[-2]))

    def intersection_update(self, *others):
        """
        Update this set with the intersection of itself and others

        Accepts both native python sets and redis Set objects as arguments

        Uses single redis pipe for the whole procedure (= very fast)
        """
        rset_keys, sets = self._split_by_type(others)
        pipe = self._pipe
        temporary_key = '__temp__'
        tmp_keys = []
        if sets:
            for index, native_set in enumerate(sets):
                tmp_key = temporary_key + str(index)
                tmp_keys.append(tmp_key)
                rset_keys.append(tmp_key)
                for element in native_set:
                    pipe.sadd(tmp_key, element)

        if rset_keys:
            rset_keys.insert(0, self.key)
            pipe.sinterstore(self.key, rset_keys)
        for tmp_key in tmp_keys:
            pipe.delete(tmp_key)
        pipe.execute()

    # TODO: Implement intersection_copy?

    def pop(self, noRemove=False):
        """
        Remove and return a random element; When ``noRemove`` is ``True``
        element will not be removed. Raises ``KeyError`` if  set is empty.
        """
        if noRemove:
            value = self._client.srandmember(self.key)
        else:
            value = self._client.spop(self.key)
        return self.type_convert(value)

    def remove(self, el):
        """
        Remove element ``el`` from this set. ``el`` must be a member,
        otherwise a ``KeyError`` is raised.
        """
        el = self.type_prepare(el)
        if not self._client.srem(self.key, el):
            raise RedisKeyError("Redis#%s, %s: Element '%s' doesn't exist" % \
                                (self._client.db, self.key, el))

    def symmetric_difference(self, *others):
        """
        Return the symmetric difference of this set and others as new set
        """
        baseKey = str(int(time()))
        key_union, key_inter = baseKey + 'union', baseKey + 'inter'

        tmp_keys = []
        redis_keys = [self.key]
        for i, other in enumerate(others):
            if isinstance(other, list):
                other = set(other)

            if isinstance(other, set):
                tmp_key = '__tmp__' + str(i)
                tmp_keys.append(tmp_key)
                redis_keys.append(tmp_key)
                for element in other:
                    self._pipe.sadd(tmp_key, element)
            elif isinstance(other, Set):
                redis_keys.append(other.key)
            else:
                raise RedisTypeError("Object must me type of set/Set")

        if redis_keys:
            self._pipe.sinterstore(key_inter, redis_keys) \
                .sunionstore(key_union, redis_keys)
            for tmp_key in tmp_keys:
                self._pipe.delete(tmp_key)

            self._pipe.sdiff([key_union, key_inter]) \
                .delete(key_union) \
                .delete(key_inter)

            return set(map(self.type_convert, self._pipe.execute()[-3]))

    def symmetric_difference_update(self, *others):
        """
        Update this set with the symmetric difference of itself and others
        """
        baseKey = str(int(time()))
        key_union, key_inter = baseKey + 'union', baseKey + 'inter'

        tmp_keys = []
        redis_keys = [self.key]
        for i, other in enumerate(others):
            if isinstance(other, list):
                other = set(other)

            if isinstance(other, set):
                tmp_key = '__tmp__' + str(i)
                tmp_keys.append(tmp_key)
                redis_keys.append(tmp_key)
                for element in other:
                    self._pipe.sadd(tmp_key, element)
            elif isinstance(other, Set):
                redis_keys.append(other.key)
            else:
                raise RedisTypeError("Object must me type of list/set/Set")

        if redis_keys:
            self._pipe.sinterstore(key_inter, redis_keys) \
                .sunionstore(key_union, redis_keys)
            for tmp_key in tmp_keys:
                self._pipe.delete(tmp_key)

            self._pipe.sdiffstore(self.key, [key_union, key_inter]) \
                .delete(key_union) \
                .delete(key_inter)

            self._pipe.execute()

    # TODO: Implement symmetric_difference_copy?

    def union(self, *others):
        """
        Return the union of this set and others as new set
        """
        rset_keys, sets = self._split_by_type(others)
        if rset_keys:
            rset_keys.append(self.key)
            data = self._client.sunion(rset_keys)
        else:
            data = self.data
        if sets:
            for native_set in sets:
                for element in native_set:
                    data.add(element)

        return data

    def update(self, *others):
        """
        Update a set with the union of itself and others
        """
        rset_keys, sets = self._split_by_type(others)
        pipe = self._pipe
        temporary_key = '__temp__'
        if sets:
            rset_keys.append(temporary_key)
            for native_set in sets:
                for element in native_set:
                    pipe.sadd(temporary_key, element)

        if rset_keys:
            rset_keys.append(self.key)
            pipe.sunionstore(self.key, rset_keys)
        pipe.delete(temporary_key)
        pipe.execute()

    def isdisjoint(self, *others):
        """
        Return ``True`` if this set and ``others`` have null intersection
        """
        rsetKeys, setElems = self._split_by_type(others)
        rsetElems = self._client.sinter(rsetKeys)
        return rsetElems.isdisjoint(setElems)

    def issubset(self, other):
        return self.data.issubset(other)

    def issuperset(self, other):
        """
        Return ``True`` if this set is contained by another set (subset)
        """
        # TODO: Implement
        raise NotImplementedError("Set.issuperset not implemented yet")

    @staticmethod
    def _split_by_type(sets, join='union'):
        """
        Separates all ``sets`` into native ``sets`` and ``Sets``
        and returns them in two lists
        """
        rset_keys, native_sets = [], []
        for s in sets:
            if isinstance(s, Set):
                rset_keys.append(s.key)
            elif isinstance(s, (set, list)):
                native_sets.append(s)
            else:
                raise RedisTypeError("Object must me type of set/list")
        return rset_keys, native_sets

    def grab(self):
        """
        Return a random element from this set;
        Return value will be of ``NoneType`` when set is empty
        """
        return self._client.srandmember(self.key)
