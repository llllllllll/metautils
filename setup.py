#!/usr/bin/env python
from distutils.core import setup
import sys

if sys.version_info.major == 2:
    raise AssertionError('metautils3 only works with Python 3')


long_description = ''
if 'upload' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='metautils3',
    version='0.1.2',
    description='Experimental utilities for working with metaclasses.',
    author='Joe Jevnik',
    author_email='joejev@gmail.com',
    packages=[
        'metautils3',
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
    url='https://github.com/llllllllll/metautils3',
    install_requires=(
        'codetransformer',
    ),
)
