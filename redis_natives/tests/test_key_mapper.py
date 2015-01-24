# from pytest import raises
# from redis import Redis
# from redis_natives import KeyMapper, List, ZSet, Scalar
# from tests import RedisWrapper


# class TestList(object):
#     def setup_method(self, method):
#         self.redis = RedisWrapper(Redis())
#         self.mapper = KeyMapper(self.redis, {
#             'users:<name>': List,
#             'queue:<int:id>': ZSet,
#             'key:<int:id>': Scalar,
#             'multi:<int:id>:<name>': Scalar
#             }
#         )
#         self.redis.flushdb()
#         self.redis.method_calls = []

#     def test_string_placeholder(self):
#         assert isinstance(self.mapper.get('users:3'), List)

#     def test_integer_placeholder(self):
#         assert isinstance(self.mapper.get('queue:1'), ZSet)

#     def test_multiple_placeholders(self):
#         assert isinstance(self.mapper.get('multi:13:chuck'), Scalar)

#     def test_non_existing_key_raises_key_error(self):
#         with raises(KeyError):
#             self.mapper.get('not_found')
