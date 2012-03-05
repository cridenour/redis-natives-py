from random import randint
from .errors import RedisKeyError
from .datatypes import RedisSortable, Comparable


class ZOrder(object):
    """
    Enum with supported sort orders of ZSet
    """
    def __new__(self):
        return ZOrder

    @property
    def ASC(self):
        return 0

    @property
    def DESC(self):
        return 1


class ZSet(RedisSortable, Comparable):
    """
    An Ordered-set datatype for Python. It's a mixture between Redis' ``ZSet``
    and a simple Set-type. Main difference is the concept of a score associated
    with every member of the set.
    """

    __slots__ = ("_key", "_client", "_pipe")

    def __init__(self, client, key, iter=[]):
        super(ZSet, self).__init__(client, key)
        if hasattr(iter, "__iter__") and len(iter):
            # TODO: What if the key already exists?
            for score, val in iter:
                self._pipe.zadd(val, score)
            self._pipe.execute()

    def __len__(self):
        return self._client.zcard(self.key)

    def __contains__(self, value):
        return self._client.zscore(self.key, value) is not None

    def __and__(self, other):
        return self._client.zrange(self.key, 0, -1) and other

    def __or__(self, other):
        return self._client.zrange(self.key, 0, -1) or other

    def __iter__(self):
        # TODO: Is there a better way than getting ALL at once?
        for score, el in self._client.zrange(self.key, 0, -1, withscores=True):
            yield (score, el)

    def __repr__(self):
        return str(self._client.zrange(self.key, 0, -1, withscores=True))

    #==========================================================================
    # Native set methods
    #==========================================================================

    def add(self, el, score):
        """
        Add element ``el`` with ``score`` to this ``ZSet``
        """
        try:
            return self._client.zadd(self.key, str(el), long(score))
        except ValueError:
            return False

    def discard(self, member):
        """
        Remove ``member`` form this set;
        Do nothing when element is not a member
        """
        self._client.zrem(self.key, member)

    def copy(self, key):
        """
        Return copy of this ``ZSet`` as new ``ZSet`` with key ``key``
        """
        # TODO: Return native set-object instead of bound redis item?
        self._client.zunionstore(key, [self.key])
        return ZSet(key, self._client)

    def clear(self):
        """
        Purge/delete all elements from this set
        """
        return self._client.delete(self.key)

    def pop(self):
        """
        Remove and return a random element from the sorted set.
        Raises ``RedisKeyError`` if  set is empty.
        """
        length = self.__len__()
        if (length == 0):
            raise RedisKeyError("ZSet is empty")
        idx = randint(0, length - 1)
        value = self._pipe.zrange(self.key, idx, idx) \
                         .zremrangebyrank(self.key, idx, idx) \
                   .execute()[0][0]
        return self.type(value)

    #==========================================================================
    # Custom methods
    #==========================================================================

    def incr_score(self, el, by=1):
        """
        Increment score of ``el`` by value ``by``
        """
        return self._client.zincrby(self.key, el, by)

    def rank_of(self, el, order=ZOrder.ASC):
        """
        Return the ordinal index of element ``el`` in the sorted set,
        whereas the sortation is based on scores and ordered according
        to the ``order`` enum.
        """
        if (order == ZOrder.ASC):
            return self._client.zrank(self.key, el)
        elif (order == ZOrder.DESC):
            return self._client.zrevrank(self.key, el)

    def score_of(self, el):
        """
        Return the associated score of element ``el`` in the sorted set.
        When ``el`` is not a member ``NoneType`` will be returned.
        """
        return self._client.zscore(self.key, el)

    def range_by_rank(self, min, max, order=ZOrder.ASC):
        """
        Return a range of elements from the sorted set by specifying ``min``
        and ``max`` ordinal indexes, whereas the sortation is based on
        scores and ordered according to the given ``order`` enum.
        """
        if (order == ZOrder.ASC):
            return self._client.zrange(self.key, min, max)
        elif (order == ZOrder.DESC):
            return self._client.zrevrange(self.key, min, max)

    def range_by_score(self, min, max):
        """
        Return a range of elements from the sorted set by specifying ``min``
        and ``max`` score values, whereas the sortation is based on scores
        with a descending order.
        """
        return self._client.zrangebyscore(self.key, min, max)

    def range_by_score_limit(self, limit=20, before=0, treshold=20):
        """
        Return a range of elements from the sorted set by specifying ``min``
        score value and the limit of items to be returned

        Note: only works for integer based scores
        """
        if not before:
            return self._client.zrevrange(self.redis_key, 0, limit,
                withscores=True)
        else:
            items = []
            while len(items) < limit:
                items += self._client.zrevrangebyscore(
                    self.redis_key,
                    before - 1,
                    before - 1 - limit - treshold,
                    withscores=True)
                if before <= 0:
                    break
                before -= limit + self.treshold

        return map(self.type_convert, items[:limit])

    def grab(self):
        """
        Return a random element from the sorted set
        """
        length = self.__len__()
        if (length == 0):
            return None
        idx = randint(0, length - 1)
        return self._pipe.zrange(self.key, idx, idx)[0]

    def intersection_copy(self, dstKey, aggregate, *otherKeys):
        """
        Return the intersection of this set and others as new set
        """
        otherKeys.append(self.key)
        return self._client.zinterstore(dstKey, otherKeys, aggregate)

    def union_copy(self, dstKey, aggregate, *otherKeys):
        otherKeys.append(self.key)
        return self._client.zunionstore(dstKey, otherKeys, aggregate)

    def remove_range_by_rank(self, min, max):
        """
        Remove a range of elements from the sorted set by specifying the
        constraining ordinal indexes ``min`` and ``max``.
        """
        return self._client.zremrangebyrank(self.key, min, max)

    def remove_range_by_score(self, min, max):
        """
        Remove a range of elements from the sorted set by specifying the
        constraining score values ``min`` and ``max``.
        """
        return self._client.zremrangebyscore(self.key, min, max)
