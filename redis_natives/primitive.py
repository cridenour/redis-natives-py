from .errors import RedisTypeError
from .datatypes import RedisDataType
from redis.exceptions import ResponseError


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
