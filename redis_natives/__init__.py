# legacy imports
from redis_natives import datatypes, natives, annotations, errors
from .set import Set
from .dict import Dict
from .zset import ZSet
from .list import List


__version__ = '0.12'
__author__ = 'Konsta Vesterinen, Peter Geil'
__all__ = (
    'datatypes',
    'natives',
    'annotations',
    'errors',
    Set,
    Dict,
    ZSet,
    List
)
