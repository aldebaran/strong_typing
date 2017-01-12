# -*- coding: utf-8 -*-

# Standard libraries
from copy import deepcopy

# strong_typing
from _textualize import TextualizedDict

class StructMeta(type):

	def __new__(mcs, name, bases, attrs, **kwargs):
		# Prepare __slots__
		attrs["__slots__"]=[]

		# If some parameters are defined
		if attrs.has_key("__ATTRIBUTES__"):
			for parameter in attrs["__ATTRIBUTES__"]:

				# Create a slot for each
				attrs["__slots__"].append("_"+parameter.id)

				# And create a descriptor class to handle their
				# get/set/default/doc based on parameter description
				class Descriptor(object):
					__doc__ ="""%s

					Default: %s

					"""%(parameter.description,\
					    str(parameter.default) if parameter.default != "" else "\"\"")

					__slots__ = ["_parameter"]

					def __init__(self, parameter):
						self._parameter = parameter

					def __get__(self, instance, owner):
						if instance is not None:
							try:
								return getattr(instance, "_"+self._parameter.id)
							except AttributeError:
								setattr(instance, "_"+self._parameter.id, self._parameter.normalizer(self._parameter.default))
								return getattr(instance, "_"+self._parameter.id)
						else:
							return self._parameter

					def __set__(self, instance, value):
						new_value = value if value is not None and value != "" else self._parameter.default
						new_value = self._parameter.normalizer(new_value)
						return setattr(instance, "_"+self._parameter.id, new_value)

					def __delete__(self, instance):
						return setattr(instance, "_"+self._parameter.id, self._parameter.normalizer(self._parameter.default))

				attrs[parameter.id] = Descriptor(parameter)

		return type.__new__(mcs, name, bases, attrs)

	def __init__(cls, name, bases, attrs, **kwargs):
		docu = """
		%s:

		Description: %s

		:Parameters:

		"""%(name, cls.__DESCRIPTION__)
		for parameter in cls.__ATTRIBUTES__:
			docu += """
			``%s``

				%s

				Default: %s

			"""%(parameter.id,\
			     parameter.description,\
			     str(parameter.default) if parameter.default != "" else "\"\"")

		cls.__doc__ = docu

	def __call__(cls, *args, **kwargs):
		# Copy constructor
		if len(args) == 1 and isinstance(args[0], cls):
			kwargs = args[0].toDict()
			args = []
		return type.__call__(cls, *args, **kwargs)

class Struct(object):
	__metaclass__= StructMeta
	__ATTRIBUTES__ = []
	__DESCRIPTION__ = ""

	def __init__(self, *args, **kwargs):
		for i in range(len(args)):
			try:
				setattr(self, self.__ATTRIBUTES__[i].id, args[i])
			except IndexError:
				msg = "__init__() takes "
				msg += "no " if len(self.__ATTRIBUTES__)==0 else "at most %d "%len(self.__ATTRIBUTES__)
				msg += "arguments (%d given)"%len(args)
				raise TypeError(msg)
		for key, value in kwargs.iteritems():
			try:
				setattr(self, key, value)
			except AttributeError, e:
				msg = "__init__() got an unexpected keyword argument '%s'"%key
				raise TypeError(msg)

	def toDict(self):
		out_dict = TextualizedDict()
		for attr in self.__ATTRIBUTES__:
			out_dict[attr.id] = getattr(self, deepcopy(attr.id))
		return out_dict

	# ─────────
	# Operators

	def __eq__(self, other):
		if not isinstance(other, Struct):
			return False
		for attribute in self.__ATTRIBUTES__:
			if getattr(self, attribute.id) != getattr(other, attribute.id):
				return False

		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	# ──────────────
	# Textualization

	def __str__(self):
		return str(self.toDict())

	def __unicode__(self):
		return unicode(self.toDict())

__all__=["Struct"]