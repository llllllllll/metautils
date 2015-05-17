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
from functools import lru_cache
from textwrap import dedent

from codetransformer.transformers import asconstants

from metautils.box import methodbox
from metautils.functional import compose


class TemplateBase(object):
    """
    A marker for `Template` types.
    """
    pass


class _TemplateMeta(type):
    """
    Constructs `ClassTemplate` objects from type specs.
    This is meta.
    """
    def __new__(mcls,
                name,
                bases,
                dict_,
                preprocess=None,
                decorators=(),
                cachesize=None,
                argname='T'):

        template_param = bases[0]
        if not isinstance(template_param, _TemplateMeta):
            raise TypeError('class template must subclass {}'.format(T))

        bases = bases[1:]
        preprocess = preprocess or (lambda *a: a)
        decorators = tuple(decorators)

        class Template(TemplateBase):
            """
            Constructs a new class that is the composition of this
            class template and a base class.

            If `adjust_name` is truthy, the name of the base class will be
            prepended with the name of the new class.
            """
            __slots__ = ()

            def __call__(self, base=type, adjust_name=True):
                dict_cpy = dict_.copy()  # We could potentially mutate this.
                inner_bases = (base,) + bases

                # This function allows us to conditionally modify the class
                # name, bases, or dict after we have recieved the base
                # class. Think of this like a second meta layer.
                name_pp, inner_bases, dict_cpy = preprocess(
                    name, inner_bases, dict_cpy
                )

                inner_base = inner_bases[0]
                transformer = asconstants(**{argname: inner_base})

                for k, v in dict_cpy.items():
                    if isinstance(v, templated):
                        # We need to change lookups to `argname`
                        # to resolve to the inner_base.
                        dict_cpy[k] = transformer(v.unboxed)

                if adjust_name:
                    # We want to have the base's name prepended to ours.
                    name_pp = base.__name__ + name_pp

                tp = compose(*decorators)(type(name_pp, inner_bases, dict_cpy))
                tp.__qualname__ = name_pp
                return tp

            if cachesize is None or cachesize >= 0:
                __call__ = lru_cache(cachesize)(__call__)

            def __repr__(self):
                return '<{cls}: {name} at 0x{id_}>'.format(
                    cls=type(self).__name__,
                    name=name,
                    id_=hex(id(self)),
                )

            __str__ = __repr__

        return Template()


# The template parameter. This uses `type.__new__` because we need a concrete
# class here, not a template.
T = type.__new__(_TemplateMeta, 'T', (object,), {
    '__doc__': dedent(
        """
        A template parameter similar to c++ class templates.

        Class templates are defined by 'subclassing' `T`.
        For example:

        >>> class MyTemplate(T):
        ...    @templated
        ...    def method(self):
        ...        print(T, 'is the template argument')

        To construct instances of your templated class, call the
        template with the class you want to subclass.

        >>> NewClass = MyTemplate(MyBaseClass)
        >>> NewClass.__base__ == MyBaseClass
        True
        >>> NewClass.__mro__ = (MyBaseClass,) + MyBaseClass.__mro__
        True

        The `templated` decorator will make the `T` resolve to the template
        argument instead of the `T` object.

        >>> NewClass().method()
        'MyBaseClass is the template argument'

        Additional arguments can be passed to the template as keyword
        arguments in the class statement.

        >>> class C(T, decorators=(mydecorator,)):
        ...     pass


        The arguments may include:

        preprocess: A function that takes the name, bases, and dict_
          of the class before it is generated and returns a new name,
          bases, and dict_. This allows you to change any of these
          class parameters before the class is constructed but after
          the template argument has been passed. The template argument
          will be `bases[0]`.

        decorators: An iterable of class decorators to apply to the
          newly constructed class object.

        cachesize: Because templates are normally used to construct
          classes dynamically, we frequently will pass the same base
          classes in multiple places. To make this more efficient,
          we can `lru_cache` the class factory. This is the argument
          that will be the `lru_cache`'s cachesize. If this is less
          than 0, no cache will be used. If this is `None`, then there
          will be no upper bounds on the cache.

        argname: The name of the template argument, by default: 'T'
          This name will be changed to resolve to the template base.
          For example:

          class C(T, argname='U'):
              @templated
              def __new__(cls):
              print('hello')
              return U.__new__(cls)
        """,
    ),
    '__slots__': (),
})


class templated(methodbox):
    """
    Marker to indicate that the method should be passed `T`
    """
    pass
