# -*- coding: utf-8 -*-

# Standard libraries
import collections
from abc import ABCMeta
import sys

# Local modules
from ._textualize import TextualizeMixin

class StructMeta(ABCMeta):

	def __new__(mcs, name, bases, attrs, **kwargs):
		# Prepare __slots__
		attrs["__slots__"]=[]

		# If some parameters are defined
		if "__ATTRIBUTES__" in attrs.keys():
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

		return ABCMeta.__new__(mcs, name, bases, attrs)

	def __init__(cls, name, bases, attrs, **kwargs):
		docu = "%s\n\n"%cls.__DESCRIPTION__
		docu += ":Parameters:\n\n"
		for parameter in cls.__ATTRIBUTES__:
			docu += "\t``%s``\n\n"%parameter.id
			docu += "\t\t%s\n\n"%parameter.description
			default_string = "``" if not isinstance(parameter.default, Struct) else ":class:`"+type(parameter.default).__name__+"`"
			default_string += str(parameter.default).replace("\n","\n\n\t\t\t") if parameter.default != "" else "\"\""
			default_string += "``" if not isinstance(parameter.default, Struct) else ""
			docu += "\t\tDefault: %s\n\n"%default_string

		cls.__doc__ = docu

	def __call__(cls, *args, **kwargs):
		# Copy constructor
		if len(args) == 1 and isinstance(args[0], cls):
			kwargs = args[0]
			args = []
		return type.__call__(cls, *args, **kwargs)

class Struct(collections.Mapping, TextualizeMixin):
	__metaclass__=StructMeta
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
		for key, value in kwargs.items():
			try:
				setattr(self, key, value)
			except AttributeError as e:
				msg = "__init__() got an unexpected keyword argument '%s'"%key
				raise TypeError(msg)

	def __getitem__(self, key):
		return getattr(self, key)

	def __setattr__(self, name, value):
		keys = list(self.keys())
		if (not name in keys) and (not name[1:] in keys):
			raise AttributeError("%s object has no attribute %s"%(self.__class__.__name__, name))
		object.__setattr__(self, name, value)

	def __iter__(self):
		for attr in self.__ATTRIBUTES__:
			yield attr.id

	def __len__(self):
		return len(self.__ATTRIBUTES__)

	# ─────────
	# Operators

	def __eq__(self, other):
		if not isinstance(other, Struct):
			return False
		for attribute in self.__ATTRIBUTES__:
			if not hasattr(other, attribute.id):
				return False
			if getattr(self, attribute.id) != getattr(other, attribute.id):
				return False

		return True

	def __ne__(self, other):
		return not self.__eq__(other)

if sys.version_info >= (3,0):
	from ._struct_v3 import Struct

__all__=["Struct"]