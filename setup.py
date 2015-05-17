#!/usr/bin/env python
from distutils.core import setup
import sys

if sys.version_info.major == 2:
    raise AssertionError('metautils only works with Python 3')


long_description = ''
if 'upload' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='metautils',
    version='0.1.0',
    description='Utilities for working with metaclasses.1',
    author='Quantopian Inc.',
    author_email='opensource@quantopian.com',
    packages=[
        'metautils',
    ],
    long_description=long_description,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Pre-processors',
    ],
    url='https://github.com/quantopian/metautils',
    install_requires=(
        'codetransformer',
    ),
)
