# -*- coding: utf-8 -*-
"""
All native datatypes.
"""

__version__ = '0.12'
__author__ = ['Peter Geil']

import os
from redis import Redis

from redis_natives.errors import RedisTypeError

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

    def generate_temporary_key(self):
        return '__tmp__' + ''.join('%02x' % ord(x) for x in os.urandom(16))

    def delete(self):
        return self._client.delete(self.key)

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
            raise RedisTypeError(
                "Target must be either type of Redis or numerical"
            )
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

    def let_expire(self, secs):
        """Let this key expire in ``secs`` seconds. After this time the
        key with its assigned value will be removed/deleted irretrievably.
        """
        self._client.expire(self.key, int(secs))

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


class SetOperatorMixin(object):
    def __and__(self, other):
        return self.intersection(other)

    def __or__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.difference(other)

    def __xor__(self, other):
        return self.symmetric_difference(other)

    def __ior__(self, other):
        self.update(other)
        return self

    def __iand__(self, other):
        self.intersection_update(other)
        return self

    def __isub__(self, other):
        self.difference_update(other)
        return self

    def __ixor__(self, other):
        self.symmetric_difference_update(other)
        return self

    def isdisjoint(self, *others):
        """
        Return ``True`` if this set and ``others`` have null intersection
        """
        return len(self.intersection(*others)) == 0

    def issuperset(self, other):
        """
        Return ``True`` if this set is contained by another set (subset)
        """
        return len(self.union(other)) == len(self)

    def parse_args(self, others):
        from .set import Set
        from .zset import ZSet
        redis_keys = [self.key]
        for i, other in enumerate(others):
            if isinstance(other, list):
                other = set(other)

            if isinstance(other, set):
                tmp_key = '__tmp__' + str(i)
                self.tmp_keys.append(tmp_key)
                redis_keys.append(tmp_key)
                for element in other:
                    if isinstance(self, ZSet):
                        self._pipe.zadd(tmp_key, element[0], element[1])
                    elif isinstance(self, Set):
                        self._pipe.sadd(tmp_key, element)
            elif isinstance(other, self.__class__):
                redis_keys.append(other.key)
            else:
                raise RedisTypeError(
                    "Object must me type of set/%s" % self.__class__.__name__
                )
        return redis_keys

    def get_pipe_value(self, i):
        return set(map(self.type_convert, self._pipe.execute()[-i - 1]))

    def _delete_temporary(self):
        keys_deleted = 0
        for temporary_key in self.tmp_keys:
            self._pipe.delete(temporary_key)
            keys_deleted += 1
        self.tmp_keys = []
        return keys_deleted


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
