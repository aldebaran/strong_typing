# -*- coding: utf-8 -*-

# Standard library
from distutils.version import StrictVersion
from copy import deepcopy

from struct import StructMeta, Struct

class VersionedStructMeta(StructMeta):

	def __init__(cls, name, bases, attrs, **kwargs):
		docu = """
		%s (current version: %s):

		Description: %s

		:Parameters:

		"""%(name, cls.__VERSION__, cls.__DESCRIPTION__)
		for parameter, version in zip(cls.__ATTRIBUTES__,cls.__ATT_VERSIONS__):
			docu += """
			``%s`` %s

				%s

				Default: %s

			"""%(parameter.id,\
			     "" if version is None else "(appeared in version %s)"%version,\
			     parameter.description,\
			     str(parameter.default) if parameter.default != "" else "\"\"")

		docu+="""

		:Deprecated parameters:

		"""
		for parameter, first_version, last_version in cls.__DEPRECATED_ATT_N_VERSIONS__:
			docu += """
			``%s``%s%s

				%s

				Default: %s

			"""%(parameter.id,\
			     "" if first_version is None else " (appeared in version %s)"%version,\
			     " (deprecated since version %s)"%last_version,\
			     parameter.description,\
			     str(parameter.default) if parameter.default != "" else "\"\"")
		cls.__doc__ = docu

	@property
	def version(cls):
		return StrictVersion(cls.__VERSION__)

class VersionedStruct(Struct):
	__metaclass__= VersionedStructMeta
	__VERSION__="1.0"
	__DESCRIPTION__ = ""
	__ATTRIBUTES__ = []
	__ATT_VERSIONS__ = []
	__DEPRECATED_ATT_N_VERSIONS__ = []

	@classmethod
	def fromDict(cls, data=dict()):
		if data.has_key("version"):
			version = StrictVersion(data.pop("version"))
			if version < cls.version:
				return cls._fromOldDict(data, version)

		return cls(**data)

	@property
	def version(self):
		return StrictVersion(self.__VERSION__)
