from collections import MutableMapping
from .errors import RedisKeyError
from .datatypes import RedisDataType


class Dict(RedisDataType, MutableMapping):
    """
    Re-implements the complete interface of the native ``dict`` datatype
    as a bound ``RedisDataType``. Use it exactly as you'd use a ``dict``.
    """

    __slots__ = ("_key", "_client", "_pipe")

    def __init__(self, client, key, iter=None, type=str):
        super(Dict, self).__init__(client, key, type)
        if hasattr(iter, "iteritems") and len(iter):
            # TODO: What if the key already exists?
            self._client.hmset(self.key, iter)

    def __len__(self):
        return self._client.hlen(self.key)

    def __iter__(self):
        for k in self._client.hkeys(self.key):
            yield k

    def __contains__(self, key):
        return self._client.hexists(self.key, key)

    def __getattr__(self, key):
        # Kinda magic-behaviour
        return self._client.hget(self.key, key)

    def __getitem__(self, key):
        val = self.type_convert(self._client.hget(self.key, key))
        if val is None:
            raise RedisKeyError("Field '" + key + "' doesn't exist")
        return val

    def __setitem__(self, key, value):
        self._client.hset(self.key, key, self.type_prepare(value))

    def __delitem__(self, key):
        if not self._client.hdel(self.key, key):
            raise RedisKeyError("Cannot delete field '" + key + \
                                "'. It doesn't exist")

    def __str__(self):
        return str(self.__repr__())

    has_key = __contains__

    def clear(self):
        self._client.delete(self.key)

    def copy(self, key):
        # TODO: Return native dict instead of bound Dict?
        return Dict(key, self._client,
                         self._client.hgetall(self.key))

    def fromkeys(self, dstKey, keys, values=""):
        self._client.hmset(dstKey, dict.fromkeys(keys, values))
        return Dict(dstKey, self._client)

    def items(self):
        # dict.items() returns a list with k,v-tuples -- and so do we
        allItems = self._client.hgetall(self.key)
        return zip(allItems.keys(), map(self.type_convert, allItems.values()))

    def iteritems(self):
        return map(self.type_convert, self._client.hgetall(self.key)) \
            .iteritems()

    def iterkeys(self):
        return iter(self._client.hkeys(self.key))

    def itervalues(self):
        return iter(map(self.type_convert, self._client.hvals(self.key)))

    def keys(self):
        return self._client.hkeys(self.key)

    # Inherited mixin methods:
    #   - get
    #   - popitem
    #   - popdef

    def setdefault(self):
        raise NotImplementedError("Method 'setdefault' is not yet implemented")

    def update(self, other, **others):
        pairs = []
        if hasattr(other, "keys"):
            for k in other:
                pairs.extend((k, other[k]))
        else:
            for (k, v) in other:
                pairs.extend((k, v))
        for k in others:
            pairs.extend((k, others[k]))
        # Using redis' bulk-hash-setter
        self._client.hsset(self.key, pairs)

    def values(self):
        return map(self.type_convert, self._client.hvals(self.key))

    def incr(self, key, by=1):
        return self._client.hincrby(self.key, key, by)
