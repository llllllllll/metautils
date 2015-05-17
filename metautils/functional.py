#
# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from functools import reduce


def _composed_doc(fs):
    """
    Generate a docstring for the composition of fs.
    """
    if not fs:
        # Argument name for the docstring.
        return 'n'

    return '{f}({g})'.format(f=fs[0].__name__, g=_composed_doc(fs[1:]))


def compose(*fs):
    """
    Compose functions together in order:

    compose(f, g, h) = lambda n: f(g(h(n)))
    """
    # Pull the iterator out into a tuple so we can call `composed`
    # more than once.
    rs = tuple(reversed(fs))

    def composed(n):
        return reduce(lambda a, b: b(a), rs, n)

    # Attempt to make the function look pretty with
    # a fresh docstring and name.
    try:
        composed.__doc__ = 'lambda n: ' + _composed_doc(fs)
    except AttributeError:
        # One of our callables does not have a `__name__`, whatever.
        pass
    else:
        # We already know that for all `f` in `fs`, there exists `f.__name__`
        composed.__name__ = '_of_'.join(f.__name__ for f in fs)

    return composed


__all__ = [
    'compose'
]
