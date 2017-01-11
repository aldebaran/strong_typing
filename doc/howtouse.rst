How to use
==========

The main purpose of ``strong_typing`` is to help you create C++-like Struct, that is to say
classes where the attributes are ALL defined and cannot be of any type. An undefined
attribute cannot be added later on.

To do this, we use several objects:
  * ``strong_typing.Struct`` which must be overridden
  * ``strong_typing.typed_parameters.<type>Parameter`` which will help us to define our attributes' types

Create a Struct
---------------

Let's create our first Struct !

::

  # mystruct.py

  from strong_typing import Struct

  class MyStruct(Struct):
    # It is not very interesting, but as a starter, let's create a
    # Struct without any attribute
    pass


::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  my_struct.any_attrib = 10 # raises AttributeError

And that's it ! You just created your first strongly-typed Struct in Python !! An
undefined attribute cannot be added at runtime.

Add parameters
--------------

Creating a Struct without parameters is not really interesting. Let's add an int and
a string to our class.

::

  # mystruct.py

  from strong_typing import Struct
  from strong_typing.typed_parameters import (IntegerParameter,
                                              StringParameter)

  class MyStruct(Struct):
    __ATTRIBUTES__=[IntegerParameter(name="my_int"),
                    StringParameter(name="my_str")]

We have now two attributes available for ``MyStruct``. When someone will try to set them,
the given value will be converted into the requested type if possible. If the given value
cannot be converted, an error will be raised.

::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  my_struct.my_int = 10.0 # is correct (10 will be stored)
  my_struct.my_int = "20" # is correct (20 will be stored)
  my_struct.my_int = "aa" # will raise an Exception
  my_struct.my_str = 10.0 # is correct ("10.0" will be stored)

There is no limit to the number of parameters. Just add as many as you want in the
__ATTRIBUTES__ list and you're good to go.


Parametrize the parameters
--------------------------

Now that we know how to add parameters, let's see how much cooler they can make our life.

For this, let's have a look at the base class of all parameters

.. autoclass:: strong_typing.typed_parameters.parameters.ParameterType

This means we can customize the default value of our parameters, but also that we can
give them any access we want.

::

  # mystruct.py

  from strong_typing import Struct
  from strong_typing.typed_parameters import IntegerParameter

  class MyStruct(Struct):
    __ATTRIBUTES__=[IntegerParameter(name="My integer", id="a", default=10),
                    IntegerParameter(name="My other integer", id="b", default=None)]


::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  print my_struct.a # prints 10
  print my_struct.b # prints None
  my_struct.a = 20
  my_struct.a = None
  print my_struct.a # prints 10

But now, you are probably wondering this:

:Question:
  How is it possible that in the first example, no value was defined as default, as there
  is no default value for ``default`` ?

Good question ! Let's examine that !

Parameters for immutable types
++++++++++++++++++++++++++++++

In our previous example, the defined parameters had a default value because numeric parameters
(int, float, ...) have a default default value.

.. autoclass:: strong_typing.typed_parameters.parameters.IntegerParameter
    :show-inheritance:

.. autoclass:: strong_typing.typed_parameters.parameters.FloatParameter
    :show-inheritance:

You can see that a default value is defined for both integer and float. But you can also notice that new arguments are available. What are they ?

.. autoclass:: strong_typing.typed_parameters.parameters.NumericParameter
    :show-inheritance:

``normalizer`` and ``range`` allow us to add new constraints on our values. We can define min
and max values, but also more specific restriction, like "odd numbers only"

::

  # mystruct.py

  from strong_typing import Struct
  from strong_typing.typed_parameters import IntegerParameter

  def make_odd(x):
    return (x/2)*2+1

  class MyStruct(Struct):
    __ATTRIBUTES__=[IntegerParameter(name="norm", normalizer=make_odd),
                    IntegerParameter(name="ranged", range=(10,20))]


::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  print my_struct.norm # prints 1
  # the default is 0, but as we only accept odd numbers,
  # 0 was transformed in 1

  print my_struct.range # prints 10
  # the default is 0, but as we only accept numbers
  # between 10 and 20, 0 became 10


Another parameter that has a default default value is BoolParameter

.. autoclass:: strong_typing.typed_parameters.parameters.BoolParameter
    :show-inheritance:

Nothing major to say about it

The last "standard" immutable available parameter is StringParameter

.. autoclass:: strong_typing.typed_parameters.parameters.StringParameter
    :show-inheritance:

The only notable difference with the previous parameters is its behavior regarding the default
value. Unlike the others, a StringParameter does not allow to set a value to ``None``, even if
it is the default value selected. A ``None`` default value will be transformed in an empty string.
Because of that, setting a string to "" is equivalent to setting it to None, ie to resetting it
to default value. As a result, if you want to allow your string to be empty, default value MUST
be "" or None (same as numeric or bool whose default must be None if you want this value to be
allowed).


::

  # mystruct.py

  from strong_typing import Struct
  from strong_typing.typed_parameters import StringParameter

  class MyStruct(Struct):
    __ATTRIBUTES__=[StringParameter(name="str1", default="default"),
                    StringParameter(name="str2")]


::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  print my_struct.str1 # prints "default"
  my_struct.str1 = "string"
  print my_struct.str1 # prints "string"
  my_struct.str1 = None # reset to default
  print my_struct.str1 # prints "default"
  my_struct.str1 = "" # ALSO reset to default
  print my_struct.str1 # prints "default"


  print my_struct.str2 # prints ""
  my_struct.str1 = "string"
  print my_struct.str1 # prints "string"
  my_struct.str1 = None # reset to default
  print my_struct.str1 # prints ""
  my_struct.str1 = "" # ALSO reset to default
  print my_struct.str1 # prints ""


A special type of immutable: Enum
+++++++++++++++++++++++++++++++++

Like in C++, it is possible to define Enums in our classes. There are several ways to implement
Enums in Python, we have chosen to use the library `enum <https://docs.python.org/3/library/enum.html>`_
which is automatically installed on Python3 (and can be installed via pip on Python2).

.. autoclass:: strong_typing.typed_parameters.parameters.EnumParameter
    :show-inheritance:

You can see a ``choices`` argument in EnumParameter constructor, this is where you will insert
your enum. You can create an Enum, but you can also more simply give a list of strings.

:Warning: The default value of an EnumParameter cannot be ``None``. If default value is not set, the first
          value of your list/enum will be used as default.

::

  # mystruct.py

  from strong_typing import Struct
  from strong_typing.typed_parameters import EnumParameter

  import enum

  class Options(enum.Enum):
    a = 1
    b = 2

  class MyStruct(Struct):
    __ATTRIBUTES__=[EnumParameter(name="choice1", choices=["a", "b"]),
                    EnumParameter(name="choice2", choices=Options, default=Choices.b)]


::

  # script.py
  from mystruct import MyStruct

  my_struct = MyStruct()
  print my_struct.choice1 # prints "a"
  my_struct.choice1 = "b"
  print my_struct.choice1 # prints "b"
  my_struct.choice1 = None # reset to default
  print my_struct.choice1 # prints "a"

  print my_struct.choice2 # prints "<Choices.a : 1>"
  my_struct.choice2 = Choices.b # works
  my_struct.choice2 = "b" # also works (but b is converted in Choices.b)


Parameters for mutable types
++++++++++++++++++++++++++++

Now let's see how are handled the mutable types.

Lists are handled through VectorParameters.

.. autoclass:: strong_typing.typed_parameters.parameters.VectorParameter

You can see a new argument ``type``. It is here to define the type of element the list will contain.

:Warning: For now, it is not possible for a list to contain other lists with a defined type. We wish we can
          add this in a latter version.

As for the strings, it is not possible to have ``None`` as a default value. It will be replaced by an empty
list. Therefore, if you set your list parameter to ``None``, it will actually be set to ``[]``. And if you
define a default value (which must be a list), then this list will be used if you set your parameter to ``None``.
However, unlike a StringParameter without any default value, it IS possible to set your list to ``[]`` even
with a non-default value: you can just remove all elements from the list, without assigning it directly a
value.


Maps are currently not handled. This will probably be done in a future version


Other Struct as parameters
++++++++++++++++++++++++++

Finally, it is possible to define a Struct as parameter of another Struct.

.. autoclass:: strong_typing.typed_parameters.parameters.StructParameter

``type`` is the type of the Struct you want to use as parameter. If ``default`` is left to
``None`` a default instance of Struct is used as default.
