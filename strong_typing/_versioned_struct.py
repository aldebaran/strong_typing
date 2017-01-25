# -*- coding: utf-8 -*-

# Standard library
from distutils.version import StrictVersion

from _struct import StructMeta, Struct

class VersionedStructMeta(StructMeta):

	def __init__(cls, name, bases, attrs, **kwargs):
		docu = "%s (current version: %s):\n\n"%(name, cls.__VERSION__)
		docu += "Description: %s\n\n"%cls.__DESCRIPTION__
		docu += ":Parameters:\n\n"
		for parameter, version in zip(cls.__ATTRIBUTES__,cls.__ATT_VERSIONS__):
			docu += "\t``%s`` %s\n\n"%(parameter.id, "" if version is None else "(appeared in version %s)"%version)
			docu += "\t\t%s\n\n"%parameter.description
			default_string = "``" if not isinstance(parameter.default, Struct) else ":class:`"+type(parameter.default).__name__+"`"
			default_string += unicode(parameter.default).replace("\n","\n\n\t\t\t") if parameter.default != "" else "\"\""
			default_string += "``" if not isinstance(parameter.default, Struct) else ""
			docu += "\t\tDefault: %s\n\n"%default_string

		if len(cls.__DEPRECATED_ATT_N_VERSIONS__) == 0:
			cls.__doc__ = docu
			return

		docu+=":Deprecated parameters:\n\n"
		for parameter, first_version, last_version in cls.__DEPRECATED_ATT_N_VERSIONS__:
			docu += "\t``%s`` %s%s\n\n"%(parameter.id,\
			                             "" if first_version is None else " (appeared in version %s)"%version,\
			                             " (deprecated since version %s)"%last_version)
			docu += "\t\t%s\n\n"%parameter.description
			default_string = unicode(parameter.default).replace("\n","\n\n\t\t\t") if parameter.default != "" else "\"\""
			docu += "\t\tDefault: %s\n\n"%default_string
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
		if "version" in data.keys():
			version = StrictVersion(data.pop("version"))
			if version < cls.version:
				return cls._fromOldDict(data, version)

		return cls(**data)

	@property
	def version(self):
		return StrictVersion(self.__VERSION__)

__all__=["VersionedStruct"]