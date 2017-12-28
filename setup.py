#!/usr/bin/python
#coding: utf-8
#(c) 2017 4Geeks Technologies, Inc.
#(c) 2017 Sergio Guzman based on stripe python

import os
import sys
from setuptools import setup, find_packages

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = ['requests >= 0.8.8']

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')


setup(name='gpayments',
      version='0.2',
      description='Client for 4Geeks Payments',
      url='https://github.com/4GeeksDev/gpayments-python',
      download_url='https://github.com/4GeeksDev/gpayments-python/tarball/master',
      author='4Geeks Technologies, Inc',
      author_email='hello@4geeks.io',
      license='MIT',
      package_data={'gpayments': ['data/ca-certificates.crt']},
      install_requires=install_requires,
      packages=find_packages(),
      keywords='4geeks payments',
      zip_safe=False)
