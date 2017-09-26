# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard library
from distutils.version import StrictVersion

# Local modules
from ._struct import StructMeta, Struct

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