#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils import setup

version = '0.12'

sdict = {
    'name': 'redis_natives',
    'version': version,
    'description': 'Exposes Redis entities as native Python datatypes. Simple, plain but powerful. Supports namespacing, indexing, and some more.',
    'long_description': 'A thin abstraction layer on top of redis-py that exposes Redis entities as native Python datatypes. Simple, plain but powerful.',
    'url': 'http://github.com/peta/redis-natives-py',
    'download_url': 'http://github.com/downloads/peta/redis-natives-py/redis-natives-py-%s.zip' % version,
    'author': ['Konsta Vesterinen', 'Peter Geil'],
    'author_email': 'konsta.vesterinen@gmail.com',
    'maintainer': 'Konsta Vesterinen',
    'maintainer_email': 'konsta.vesterinen@gmail.com',
    'keywords': ['Redis', 'key-value store', 'redis-py', 'datatypes', 'natives', 'helper'],
    'license': 'BSD',
    'packages': ['redis_natives'],
    'requires': ['redis (>=2.0)'],
    'test_suite': 'tests.all_tests',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Database'],
}


setup(**sdict)
