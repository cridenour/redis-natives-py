'''
Exceptions thrown by ``redis_natives``.
'''

__version__ = '0.1'
__author__ = ['Peter Geil', 'Konsta Vesterinen']


class RedisTypeError(TypeError):
    pass


class RedisKeyError(TypeError):
    pass


class RedisValueError(ValueError):
    pass
