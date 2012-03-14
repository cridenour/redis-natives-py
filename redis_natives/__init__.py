# legacy imports
from redis_natives import datatypes, natives, annotations, errors
from .set import Set
from .dict import Dict
from .zset import ZSet
from .list import List
from .scalar import Scalar
from .key_mapper import KeyMapper


__version__ = '0.12'
__author__ = 'Konsta Vesterinen, Peter Geil'
__all__ = (
    'datatypes',
    'natives',
    'annotations',
    'errors',
    Dict,
    List,
    Scalar,
    Set,
    ZSet,
    KeyMapper
)
