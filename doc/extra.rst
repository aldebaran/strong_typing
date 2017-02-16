Extra-functionalities
=====================

Auto-documentation
------------------

Classes and parameters create their docstrings based on:
 * Their ``description`` attribute for :py:class:`ParameterType`
 * The ``__DESCRIPTION__`` field for :py:class:`Struct`

Then you can use this docstring to generate documentation with sphinx, you can
visualize it in a Python shell, and so on.

:Example:

	Let's write a Struct like this:

	.. literalinclude:: mystruct.py


	We can then generate its documentation using this

	.. code-block:: rest

		.. doc.rst

		.. automodule:: mystruct
			:members:

	Which will generate the following output:

	.. automodule:: mystruct
		:members:


.. Versioned struct
.. ----------------

.. When a :py:class:`Struct` is defined, your users might want to store those values in a file, or to serialize
.. it before being stored and or saved. You might also want to use those :py:class:`Struct` to communicate with
.. others. But what if those "others" have an older version of your Struct. A version with different attributes,
.. with a different API ?

.. This is the reason why was added the :py:class:`VersionedStruct` class. It is a :py:class:`Struct` that has
.. a ``__VERSION__`` attribute. Using this, you can easilly compare if the serialized data you are receiving
.. (which must contain a ``version`` attribute as well) fits your class definition version.