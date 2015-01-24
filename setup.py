#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

sdict = {
    'name': 'redis_natives',
    'version': find_version('redis_natives', '__init__.py'),
    'description': 'Exposes Redis entities as native Python datatypes. Simple, plain but powerful. Supports namespacing, indexing, and some more.',
    'long_description': long_description,
    'url': 'http://github.com/cridenour/redis-natives-py',
    'download_url' : 'http://github.com/downloads/cridenour/redis-natives-py/redis-natives-py-%s.zip' % find_version('redis_natives', '__init__.py'),
    'author' : 'Peter Geil',
    'author_email' : 'code@petergeil.name',
    'maintainer' : 'Chris Ridenour',
    'maintainer_email' : 'chrisridenour@gmail.com',
    'keywords' : ['Redis', 'key-value store', 'redis-py', 'datatypes', 'natives', 'helper'],
    'license' : 'BSD',
    'packages' : ['redis_natives'],
    'include_package_data': True,
	'requires': ['redis (>=2.4)'],
    'test_suite' : 'redis_natives.tests',
    'tests_require': ['pytest'],
    'cmdclass': {'test': PyTest},
    'classifiers' : [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Database'],
    'extras_require': {
        'testing': ['pytest'],
    }
}


setup(**sdict)
