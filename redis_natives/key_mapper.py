# from werkzeug.routing import Map, Rule
# from werkzeug.exceptions import NotFound


# class KeyMapper(object):
#     rules = {}

#     def __init__(self, redis, rules={}):
#         self.redis = redis
#         map = Map()
#         for rule, type in rules.items():
#             map.add(Rule('/%s' % rule, endpoint=type))

#         self.map = map.bind('redis')

#     def get(self, name):
#         try:
#             match = self.map.match(name)

#             return match[0](self.redis, name)
#         except NotFound:
#             raise KeyError(name)
