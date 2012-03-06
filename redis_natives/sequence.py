from .errors import RedisValueError, RedisTypeError
from .datatypes import RedisSortable
from collections import Sequence


class Sequence(RedisSortable, Sequence):
    """
    Sequence datatype that implements all functions of ``Redis list`` datatypes.
    Compared to ``List``, a ``Sequence`` doesn't try to meme a native
    ``list`` datatype and instead exposes all native functionalities of Redis
    for working with list datatypes.

    A typical use-case where this functionality is needed are f.e. FIFO/LIFO
    processings. (stacks/queues)
    """

    __slots__ = ("_key", "_client", "_pipe")

    def __init__(self, client, key, reset=False):
        super(Sequence, self).__init__(client, key)
        # Removed the check for initial iter-values because Sequences
        # will be used for queue-specific stuff and because it matters
        # if b-lpop/b-rpop, I let it up to the user how to insert initials
        if reset:
            # When key already exists: FLush the bastard
            self._client.delete(self.key)

    #===========================================================================
    # Built-in/Required methods
    #===========================================================================

    def __str__(self):
        return str(self._client.lrange(self.key, 0, -1))

    __repr__ = __str__

    def __contains__(self, el):
        # As long as redis doesn't support lookups by value, we
        # have to use this inefficient workaround
        return el in self._client.lrange(self.key, 0, -1)

    def __iter__(self):
        #for el in self._client.lrange(self.key, 0, -1):
        for i in range(self.__len__()):
            yield self._client.lindex(self.key, i)

    def __len__(self):
        return self._client.llen(self.key)

    def __reversed__(self):
        li = self._client.lrange(self.key, 0, -1)
        li.reverse()
        return iter(li)

    def __getitem__(self, idx):
        return self._client.lindex(self.key, idx)

    def __getslice__(self, start, end):
        return self._client.lrange(self.key, start, end)

    def count(self, el):
        return self._client.lrange(self.key, 0, -1).count(el)

    def index(self, el):
        # Expensive -- but there's no other way
        return self._client.lrange(self.key, 0, -1).index(el)

    #==========================================================================
    # Custom methods
    #==========================================================================

    def push_head(self, el):
        """
        Push value ``el`` in *front* of this list.
        """
        self._client.lpush(self.key, el)
        return 0

    def push_tail(self, el):
        """
        Push value ``el`` at the *end* of this list.
        """
        # Subtracting 1 so that we get the real index within the sequence
        return self._client.rpush(self.key, el) - 1

    def pop_head(self):
        """
        Remove and return the *first* element from this list
        """
        return self._client.lpop(self.key)

    def pop_tail(self):
        """
        Remove and return the *last* element from this list
        """
        return self._client.rpop(self.key)

    def bpop_head(self, keys=[], timeout=0):
        """
        ``pop_tail`` a value off of the first non-empty list named in the
        ``keys`` list and return it together with the ``key`` that unblocked
        it as a two-element tuple.

        If none of the lists in ``keys`` has a value to ``pop_tail``, then
        block for ``timeout`` seconds, or until a value gets pushed on to
        one of the lists.

        If ``timeout`` is 0, then block indefinitely.
        """
        # For more informations about blocking operations see:
        # ---> http://code.google.com/p/redis/wiki/BlpopCommand
        return self._client.blpop(keys.insert(0, self.key), timeout)

    def bpop_tail(self, keys=[], timeout=0):
        """
        ``pop_tail`` a value off of the first non-empty list named in the
        ``keys`` list and return it together with the ``key`` that unblocked
        it as a two-element tuple.

        If none of the lists in ``keys`` has a value to ``pop_tail``, then
        block for ``timeout`` seconds, or until a value gets pushed on to
        one of the lists.

        If ``timeout`` is 0, then block indefinitely.
        """
        # For more informations about blocking operations see:
        # ---> http://code.google.com/p/redis/wiki/BlpopCommand
        return self._client.brpop(keys.insert(0, self.key), timeout)

    def pop_tail_push_head(self, dstKey):
        """
        Removes the *last* element from this list, ``push_head`` it
        to the list with a key named ``dstKey`` (atomically) and finally
        return the value.
        """
        return self._client.rpoplpush(self.key, dstKey)

    def range(self, start, end):
        """
        Returns all elements whose indexes are within the range of ``start``
        and ``end``. When ``start`` or ``end`` are negative the range is
        fetched relative from the end of this list.
        """
        if type(start) is type(end) is int:
            return self.__getslice__(start, end)
        else:
            raise RedisTypeError("Range indexes must be type of 'int'")

    def trim(self, start, end):
        """
        Removes/trims all values except those within the index range of
        ``start`` and ``end``.
        """
        if type(start) is type(end) is int:
            self._client.ltrim(self.key, start, end)
        else:
            raise RedisTypeError("Range indexes must be type of 'int'")

    def remove(self, val, n=1, all=False):
        """
        Removes ``n`` occurences of value ``el``. When ``n`` is ``0``
        all occurences will be removed. When ``n`` is negative the lookup
        start at the end, otherwise from the beginning.

        Returns number of removed values as ``int``.
        """
        if all:
            if self._client.lrem(self.key, val, 0):
                return None
        elif isinstance(n, int):
            if self._client.lrem(self.key, val, n):
                return None
        else:
            raise RedisTypeError("Argument 'count' must be type of 'int'")
        raise RedisValueError("Value '" + str(val) + "' not present")
