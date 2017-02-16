**strong_typing** is a Python package containing some classes to create strongly typed structures in Python

``strong_typing`` in a few words
--------------------------------

In Python, all variables are weakly typed, which means that a variable can take all values of
any type. The Python interpreter will then infer at runtime which operations this variable can
undergo depending on what it contains. This is called "type inference".

This can be a problem in different situations

 - A function that does not receive the expected type as input
 - A variable or a class attribute whose type is changed through assignment

To avoid functions being called with bad arguments, you can use Python's `typing module <https://docs.python.org/3/library/typing.html>`_) (however only with Python3).
To check if a variable is not incorrectly used, you can install and run `mypy module <http://mypy.readthedocs.io/en/latest/>`_).

But if the latest is great for static check (without running the code), it does not work
on the code you don't own.

If, for instance you design a class expecting a certain type of attributes, ``mypy`` can very
easily detect if you don't mistakenly override these attributes with wrong typed data.
But if you put this class in a Python package and that someone else uses it, there
is no way to be sure they will respect your attribute's type.
To make sure they do, you would need to define a descriptor's class for each attribute and
define a setter function protecting your value against abusive set. That's what we did :)

In the end, your class could look like this:

::

  class MyTypedStruct(Struct):
    __ATTRIBUTES__ = [IntegerParameter(name="my_int"),
                      FloatParameter(name="my_float")]
    __DESCRIPTION__ = "A sample of class with typed attributes"

Want to know more ?
-------------------

Find the complete documentation `here <http://doc.aldebaran.lan/doc/master/strong_typing/howtouse.html>`_.

You can also download the code from `here <https://gitlab.aldebaran.lan/sambrose/py_strong_typing.git>`_
or install the latest release with:

	``pip install strong_typing --find-links=http://10.0.2.107/pypi --extra-index-url http://10.0.2.107/pypi --trusted-host 10.0.2.107``