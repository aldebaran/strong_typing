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
	"""
	Base type for parameters

	:param name: Name of the parameter
	:param description: Description of the parameter
	:param default: Default value
	:param id: Token used to access the parameter

	If ``default`` is ``None``, it means the parameter is optional and
	can have ``None`` as a value. Otherwise, setting the parameter to
	``None`` actually resets it to the default value.

	If ``id`` is ``None``, it will by default be the name of the
	parameter turned into a snakecase string. Otherwise, the only
	requirement is for the id to be a snakecase string (it doesn't have
	to be related to the parameter's name)

	:Example:
		If name is 'My Parameter', then id will be 'my_parameter',
		and its value will be accessible by calling
		<owning_class>.my_parameter
	"""
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

class NumericParameter(ParameterType):
	"""
	Base type for numeric parameters

	:param normalizer: Extra-verification function
	:param range: Couple of values representing the lowest and
	              highest possible values the parameter can take
	              It is possible to define only one of the two and
	              leave the other to None to have only a minimum or
	              only a maximum

	``normalizer`` is a user-defined function allowing him to perform
	an extra-verification on the inserted value. For instance, a function
	can be added to accept only odd numbers, or perfect square number. In
	case the inserted value does not match the requirement, the function
	must provide a valid value instead of the inserted one.
	"""
	def __init__(self, name, description, default, normalizer,
	                   range=(None,None), id = None):
		ParameterType.__init__(self, name, description, default, id)
		self.default = default
		f = lambda x: None if x is None else normalizer(x)
		self.range   = tuple(map(f, range))

		def _normalizer(x):
			if x is None:
				return None
			x = normalizer(x)
			if not self.range[0] is None and x < self.range[0]:
				x = self.range[0]
			if not self.range[1] is None and x > self.range[1]:
				x = self.range[1]
			return x

		self._normalizer = _normalizer

class IntegerParameter(NumericParameter):
	"""
	Integer parameter
	"""
	def __init__(self, name="", description="", default=0,
		               normalizer=None, range=(None,None),
		               id = None):
		if normalizer is not None:
			_normalizer = lambda x:int(normalizer(int(x)))
		else:
			_normalizer = int
		NumericParameter.__init__(self, name, description, default,
		                                _normalizer, range, id)

class FloatParameter(NumericParameter):
	"""
	Float parameter
	"""
	def __init__(self, name="", description="", default=0.0,
		               normalizer=None, range=(None,None),
		               id = None):
		if normalizer is not None:
			_normalizer = lambda x:float(normalizer(float(x)))
		else:
			_normalizer = float
		NumericParameter.__init__(self, name, description, default,
		                                _normalizer, range, id)

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
	"""
	Parameter describing a set of choices

	:param choices: Set of possible choices. It can be a list of strings, or an
	enum.Enum
	:param default: Default value
	If ``default`` is ``None``, the first of the available choices is selected as
	default.
	"""
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
	"""
	Handles list

	:param type: Type of the elements stored in the list
	"""
	def __init__(self, type, name="", description="", default=None, id = None):
		default = list(default) if default is not None else list()
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			return TypedList(type, x)

		self._normalizer = normalizer

class StructParameter(ParameterType):
	"""
	Handles a Struct

	:param type: Type of the Struct to be used
	"""
	def __init__(self, type, default=None, name="", description="", id = None):
		default = type(default) if isinstance(default, type) else type()
		ParameterType.__init__(self, name, description, default, id)

		def normalizer(x):
			return type(x)

		self._normalizer = normalizer
