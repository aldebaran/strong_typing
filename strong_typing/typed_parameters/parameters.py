# -*- coding: utf-8 -*-

# Standard libraries
import re

# Third-party libraries
import enum

# strong_typing
from ..typed_containers import TypedList

# ───────────────────────────────── Helpers ────────────────────────────────── #

def isSnakecase(s):
	return re.match(r"[a-z][a-z0-9_]*?[a-z0-9]?",s) is not None

def snakecase(s):
	return re.sub(r"[^a-z0-9]", "_", s.lower())

# ──────────────────────────── Type classes ────────────────────────────────── #

class ParameterType(object):
	def __init__(self, name, description, default, id = None):
		self.name = name
		self.description = description
		self.default = default
		if id is None:
			# By default derive the id from the name
			self.id = snakecase(name)
		else:
			assert(isSnakecase(id))
			self.id = id

	@property
	def normalizer(self):
		"""
		Coerces close values not in the domain to valid values.

		Also converts textual representation of the parameter to a valid value.
		"""

		if hasattr(self, "_normalizer"):
			return self._normalizer
		else:
			raise NotImplementedError

class NumeralParameter(ParameterType):
	def __init__(self, name, description, default, normalizer,
	                   range=(None,None), id = None):
		ParameterType.__init__(self, name, description, default, id)
		self.default = default
		self.range   = range

		def _normalizer(x):
			if x is None:
				return None
			x = normalizer(x)
			if not range[0] is None and x < range[0]:
				x = range[0]
			if not range[1] is None and x > range[1]:
				x = range[1]
			x = normalizer(x) # just in case range is not in the good type...
			return x

		self._normalizer = _normalizer

class IntegerParameter(NumeralParameter):
	def __init__(self, name="", description="", default=0, range=(None,None),
		               normalizer=int, id = None):
		NumeralParameter.__init__(self, name, description, default,
		                                normalizer, range, id)

class FloatParameter(NumeralParameter):
	def __init__(self, name="", description="", default=0.0, range=(None,None),
		               normalizer=float, id = None):
		NumeralParameter.__init__(self, name, description, default,
		                                normalizer, range, id)

class BoolParameter(ParameterType):
	def __init__(self, name="", description="", default=False, id = None):
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			if x is None:
				return None
			try:
				if int(x)==0:
					return False
			except ValueError:
				pass

			return False if x in ["False", "false"] else bool(x)

		self._normalizer = normalizer

class EnumParameter(ParameterType):
	class EnumFromList(enum.Enum):
		def __eq__(self, other):
			if isinstance(other, str):
				return self.name == other
			elif isinstance(other, type(self)):
				return self.name == other.name
			else:
				return False

		def __ne__(self, other):
			return not self.__eq__(other)

		def __str__(self):
			return str(self.name)

		def __unicode__(self):
			return unicode(self.name)

	def __init__(self, choices, name="", description="", default=None, id = None):
		if isinstance(choices, list):
			choices=enum.EnumMeta("_local_enum_from_list_",
				                  (EnumParameter.EnumFromList,),
				                  dict(
				                    [[choices[i], i] for i in range(len(choices))]
				                  )
				                 )
		elif not isinstance(choices, type) or not issubclass(choices, enum.Enum):
			# If choices is not a class and not an enum
			raise TypeError("Enum's choices can only be a list or an enum.Enum")

		self.choices = choices
		if len(list(self.choices))==0:
			raise TypeError("Enum's choices cannot be an empty")

		if isinstance(default, enum.Enum):
			default = self.choices(default)
		elif default is not None:
			default = self.choices[default]
		else:
			default = list(self.choices)[0]

		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			if isinstance(x, enum.Enum):
				return self.choices(x)
			else:
				return self.choices[x]

		self._normalizer = normalizer

class StringParameter(ParameterType):
	def __init__(self, name="", description="", default=None, id = None):
		default = str(default) if default is not None else ""
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			return str(x)

		self._normalizer = normalizer

class VectorParameter(ParameterType):
	def __init__(self, type, name="", description="", default=None, id = None):
		default = list(default) if default is not None else list()
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			return TypedList(type, x)

		self._normalizer = normalizer

class StructParameter(ParameterType):
	def __init__(self, type, default=None, name="", description="", id = None):
		default = type(default) if isinstance(default, type) else type()
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			return type(x)

		self._normalizer = normalizer
