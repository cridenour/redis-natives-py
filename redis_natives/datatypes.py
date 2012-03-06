# -*- coding: utf-8 -*-
"""
All native datatypes.
"""

__version__ = '0.11'
__author__ = ['Peter Geil', 'Konsta Vesterinen']

from collections import MutableMapping, Sequence

from redis import Redis
from redis.exceptions import ResponseError

from redis_natives.errors import RedisTypeError, RedisKeyError, RedisValueError

__all__ = (
    "Primitive",
    "Set",
    "ZSet",
    "ZOrder",
    "Dict",
    "List",
    "Sequence"
)


class RedisDataType(object):
    """
    Base class for all Redis datatypes. Implements basic stuff that is shared
    by all Redis datatypes (derived from it).
    """

    __slots__ = ("_pipe", "_client", "_key")

    def __init__(self, client, key, type=str):
        if not isinstance(key, str):
            raise RedisTypeError("Key must be type of string")
        self._key = str(key)
        self._client = client
        # Offer it by for bulk-commands
        self._pipe = client.pipeline()
        self.type = type
        if type is bool:
            self.type_convert = lambda a: bool(int(a))
        else:
            self.type_convert = type

    @property
    def key(self):
        """
        The redis-internal key name of this object
        """
        return self._key

    @key.setter
    def key(self, val):
        self.rename(val)

    def type_prepare(self, val):
        if self.type is bool:
            return int(val)
        return val

    @property
    def exists(self):
        """Returns ``True`` if an associated entity for this ``RedisDataType``
        instance already exists. Otherwise ``False``.
        """
        return self._client.exists(self.key)

    @property
    def redis_type(self):
        """Return the internal name of a datatype. (Specific to Redis)
        """
        return self._client.type(self.key)

    def move(self, target):
        """Move this key with its assigned value into another database with
        index ``target``.
        """
        if isinstance(target, Redis):
            dbIndex = target.db
        elif isinstance(target, (int, long)):
            dbIndex = target
        else:
            raise RedisTypeError("Target must be either type of Redis or numerical")
        return self._client.move(self.key, dbIndex)

    def rename(self, newKey, overwrite=True):
        """Rename this key into ``newKey``
        """
        oldKey = self.key
        if overwrite:
            if self._client.rename(oldKey, newKey):
                self.key = newKey
                return True
        else:
            if self._client.renamenx(oldKey, newKey):
                self.key = newKey
                return True
        return False

    @property
    def expiration(self):
        """The time in *s* (seconds) until this key will be automatically
        removed due to an expiration clause set before.
        """
        return self._client.ttl(self.key)

    def let_expire(self, nSecs):
        """Let this key expire in ``nSecs`` seconds. After this time the
        key with its assigned value will be removed/deleted irretrievably.
        """
        self._client.expire(self.key, int(nSecs))

    def let_expire_at(self, timestamp):
        """Let this key expire exactly at time ``timestamp``. When this time
        arrives the key with its assigned value will be removed/deleted
        irretrievably.
        """
        self._client.expireat(self.key, int(timestamp))


class RedisSortable(RedisDataType):
    """
    A ``RedisSortable`` base class for bound Redis ``RedisSortables``.
    (Will probably be removed soon)
    """
    def sort(self):
        # TODO: Implement using redis' generic SORT function
        raise NotImplementedError("Method 'sort' not yet implemented")


class Primitive(RedisDataType):
    '''
    A ``Primitive`` is basically the same as a ``str``. It offers all the
    methods of a ``str`` plus functionality to increment/decrement its value.
    '''

    __slots__ = ("_key", "_client", "_pipe")

    def __init__(self, client, key, value=None):
        super(Primitive, self).__init__(client, key)
        if value is not None:
            self.value = str(value)

    #==========================================================================
    # Built-in methods
    #==========================================================================

    def __add__(self, val):
        return self.value + val

    def __iadd__(self, val):
        self._client.append(self.key, val)
        return self

    def __contains__(self, val):
        return val in self.value

    def __eq__(self, val):
        return self.value == val

    def __hash__(self):
        return self.value.__hash__()

    def __len__(self):
        return self.value.__len__()

    def __mul__(self, val):
        return self.value * val

    def __reduce__(self, *ka, **kwa):
        return self.value.__reduce__(*ka, **kwa)

    def __str__(self):
        return self.value

    __repr__ = __str__

    def _formatter_field_name_split(self, *ka, **kwa):
        return self.value._formatter_field_name_split(*ka, **kwa)

    def _formatter_parser(self, *ka, **kwa):
        return self.value._formatter_parser(*ka, **kwa)

    def __getslice__(self, i, j):
        return self._client.substr(self.key, i, j)

    def __getattr__(self, name):
        # Delegate all other lookups to str
        return self.value.__getattribute__(name)

    #==========================================================================
    # Custom methods
    #==========================================================================

    @property
    def value(self):
        '''The current value of this object
        '''
        return self._client.get(self.key)

    @value.setter
    def value(self, value):
        self._client.set(self.key, value)

    @value.deleter
    def value(self):
        self._client.delete(self.key)

    def incr(self, by=1):
        '''
        Increment the value by value ``by``. (1 by default)
        '''
        # Should I check for by-value and use 'incr' when appropriate?
        try:
            return self._client.incr(self.key, by)
        except ResponseError:
            raise RedisTypeError(
                "Cannot increment Primitive with string-value")

    def decr(self, by=1):
        '''
        Decrement the value by value ``by``. (1 by default)
        '''
        # Should I check for by-value and use 'decr' when appropriate?
        try:
            return self._client.decrby(self.key, by)
        except ResponseError:
            raise RedisTypeError(
                "Cannot decrement Primitive with string-value")


class Comparable(object):
    def __gt__(self, other):
        return self.__len__() > len(other)

    def __lt__(self, other):
        return self.__len__() < len(other)

    def __ge__(self, other):
        return self.__len__() >= len(other)

    def __le__(self, other):
        return self.__len__() <= len(other)


if __name__ == "__main__":
    pass
