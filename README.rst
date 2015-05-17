metautils
=========

Utilities for writing and composing metaclasses.

Template Model
-----------------------

Why do we need or want to write class templates.

Consider the two metaclasses.

.. code:: python

    class AllLower(type):
        def __new__(mcls, name, bases, dict_):
            dict_ = {k.lower(): v for k, v in dict_.items()}
            return super().__new__(mcls, name, bases, dict_)


    class MethodCatcher(type):
        def __new__(mcls, name, bases, dict_):
            dict_['methods'] = [v for v in dict_.values() if callable(v)]
            return super().__new__(mcls, name, bases, dict_)

What would we do if we wanted to make a class that used *BOTH* of these
metaclasses? Using a class that subclasses both ``AllLower`` and
``MethodCatcher`` does not work, what we want is a way to chain them.

With the class template model, we could have written our metaclasses
as:

.. code:: python

    from metautils import T, templated

    class AllLower(T):
        @templated
        def __new__(mcls, name, bases, dict_):
            dict_ = {k.lower(): v for k, v in dict_.items()}
            return super().__new__(mcls, name, bases, dict_)


    class MethodCatcher(T):
        @templated
        def __new__(mcls, name, bases, dict_):
            dict_['methods'] = [v for v in dict_.values() if callable(v)];
            return super().__new__(mcls, name, bases, dict_)


Python 2 style super calls will also work, like: ``super(AllLower, mcls)``.
We can write the above classes without using super by delagating to ``T``
just like we would delegate to a concrete class, for example:

.. code:: python

   from metautils import T, templated

    class AllLower(T):
        @templated
        def __new__(mcls, name, bases, dict_):
            dict_ = {k.lower(): v for k, v in dict_.items()}
            return T.__new__(mcls, name, bases, dict_)


    class MethodCatcher(T):
        @templated
        def __new__(mcls, name, bases, dict_):
            dict_['methods'] = [v for v in dict_.values() if callable(v)];
            return T.__new__(mcls, name, bases, dict_)


Inside the context of a templated function, ``T`` with refer to the concrete
class that was used to instantiate an instance of the template.
Another name that will be changed out from under you is the class name
itself. When you are in the context of a method, the class name will actually
resolve to the concrete type.

Now we can define classes that use *BOTH* of these metaclasses like so:

.. code:: python

    class C(object, metaclass=MethodCatcher(AllLower())):
        def F():
            pass

        def g():
            pass

        a = 'a'
        B = 'b'

We can see that this applied the composition of the metaclasses.

.. code:: python

    >>> C.f
    <function __main__.C.F>
    >>> C.g
    <function __main__.C.g>
    >>> C.b
    'b'
    >>> C.a
    'a'
    >>> C.methods
    [<function __main__.C.g>, <function __main__.C.F>]

The order that the metaclasses are composed is explicit as they act as
transformers over each other.


``Template``
--------------------

While the previous example only showed metaclasses, you can use this for any
class; however, it is most useful for metaclasses where having a compatible
metaclass hierarchy is important.

A ``Template`` is a callable that takes a ``type`` object and
returns a new ``type`` object. It takes the following arguments:

-  ``base``: A type object. ``default``: ``type``.
-  ``adjust_name``: Should we prepend the name of the ``base`` to the
   new type object. ``default``: ``True``.

These can be chained together with any concrete metaclass at the end,
e.g.:

.. code:: python

    new_class = m(n,p(q(...z(type)...)))

You can also use the compose function to do this:

.. code:: python

    from metautils import compose

    new_class_template = compose(m, n, p, q, ..., z)
