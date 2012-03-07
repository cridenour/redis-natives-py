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

    def difference(self, other):
        """
        Return the difference between this set and other as new set
        """
        rset_keys, set_elems = self._splitBySetType(other)
        if rset_keys:
            rset = self._client.sunion(rset_keys)
        else:
            rset = self
        data = rset.data
        if set_elems:
            data -= set_elems
        return data

    def difference_update(self, *others):
        """
        Remove all elements of other sets from this set
        """
        pipe = self._pipe
        pipe.delete(self.key)
        for el in self.difference(*others):
            pipe.sadd(self.key, el)
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
        rsetKeys, set_elems = self._splitBySetType(*others)
        data = self.data
        if set_elems:
            data = data.intersection(set_elems)
        return data

    def intersection_update(self, *others):
        """
        Update this set with the intersection of itself and others
        """
        pipe = self._pipe
        pipe.delete(self.key)
        for el in self.intersection(*others):
            pipe.sadd(self.key, el)
        pipe.execute()
        return self

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
        rset_keys, set_elems = self._splitBySetType(*others)
        # server-side caching
        baseKey = str(int(time()))
        keyUnion, keyInter = baseKey + 'union', baseKey + 'inter'
        if rset_keys:
            rsetElems = self._pipe.sinterstore(keyUnion, rset_keys) \
                                  .sunionstore(keyInter, rset_keys) \
                                  .sdiff([keyUnion, keyInter]) \
                                  .delete(keyUnion) \
                                  .delete(keyInter) \
                            .execute()[2]
        data = self.data
        if set_elems:
            data = data.symmetric_difference(set_elems)
        return data

    def symmetric_difference_update(self, *others):
        """
        Update this set with the symmetric difference of itself and others
        """
        pipe = self._pipe
        # Probably faster than getting another diff + iteratively deleting then
        pipe.delete(self.key)
        for el in self.symmetric_difference(*others):
            pipe.sadd(self.key, el)
        pipe.execute()
        return self

    # TODO: Implement symmetric_difference_copy?

    def union(self, *others):
        """
        Return the union of this set and others as new set
        """
        rset_keys, set_elems = self._splitBySetType(*others)
        if rset_keys:
            rset = self._client.sunion(rset_keys)
        else:
            rset = self
        if set_elems:
            data = rset.data
            for element in set_elems:
                data.add(element)
        return data

    def update(self, *others):
        """
        Update a set with the union of itself and others
        """
        pipe = self._pipe
        pipe.delete(self.key)
        for el in self.union(*others):
            pipe.sadd(self.key, el)
        pipe.execute()

    def isdisjoint(self, *others):
        """
        Return ``True`` if this set and ``others`` have null intersection
        """
        rsetKeys, setElems = self._splitBySetType(*others)
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
    def _splitBySetType(*sets):
        """
        Separates all ``sets`` into native ``sets`` and ``Sets``
        and returns them in two lists
        """
        rsetKeys, set_elements = [], []
        for s in sets:
            if isinstance(s, Set):
                rsetKeys.append(s.key)
            elif isinstance(s, (set, list)):
                set_elements.extend(s)
            else:
                raise RedisTypeError("Object must me type of set/list")
        return rsetKeys, set(set_elements)

    def grab(self):
        """
        Return a random element from this set;
        Return value will be of ``NoneType`` when set is empty
        """
        return self._client.srandmember(self.key)
