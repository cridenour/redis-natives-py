from .errors import RedisTypeError
from .datatypes import RedisDataType
from redis.exceptions import ResponseError


class Scalar(RedisDataType):
    '''
    A ``Scalar`` is basically the same as a ``str``. It offers all the
    methods of a ``str`` plus functionality to increment/decrement its value.
    '''

    def __init__(self, client, key, type=str, value=None):
        super(Scalar, self).__init__(client, key, type)
        if value is not None:
            self.value = str(value)

    def __add__(self, val):
        return self.value + val

    def __iadd__(self, val):
        if self.type == int:
            self.value += val
        else:
            self._client.append(self.key, val)
        return self

    def __contains__(self, val):
        return val in self.value

    def __eq__(self, val):
        return self.value == val

    def __hash__(self):
        return self.value.__hash__()

    def __len__(self):
        return self._client.strlen(self.key)

    def __mul__(self, val):
        return self.value * val

    def __reduce__(self, *ka, **kwa):
        return self.value.__reduce__(*ka, **kwa)

    def __str__(self):
        return self.value

    def _formatter_field_name_split(self, *ka, **kwa):
        return self.value._formatter_field_name_split(*ka, **kwa)

    def _formatter_parser(self, *ka, **kwa):
        return self.value._formatter_parser(*ka, **kwa)

    def __getslice__(self, i, j):
        if i == j == 0:
            return ''

        if i is None:
            i = 0
        if j is None:
            j = -1
        else:
            j -= 1
        return self._client.substr(self.key, i, j)

    def __getattr__(self, name):
        # Delegate all other lookups to str
        return self.value.__getattribute__(name)

    @property
    def value(self):
        '''The current value of this object
        '''
        return self.type_convert(self._client.get(self.key))

    @value.setter
    def value(self, value):
        self._client.set(self.key, self.type_prepare(value))

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
                "Cannot increment Scalar with string-value")

    def decr(self, by=1):
        '''
        Decrement the value by value ``by``. (1 by default)
        '''
        # Should I check for by-value and use 'decr' when appropriate?
        try:
            return self._client.decrby(self.key, by)
        except ResponseError:
            raise RedisTypeError(
                "Cannot decrement Scalar with string-value")
