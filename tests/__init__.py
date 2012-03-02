class RedisWrapper(object):
    method_calls = []

    def __init__(self, redis):
        self._redis = redis

    def __getattr__(self, name):
        self.method_calls.append(name)
        return getattr(self._redis, name)
