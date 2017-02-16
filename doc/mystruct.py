# mystruct.py

import enum
from strong_typing import Struct
from strong_typing.typed_parameters import *
from strong_typing.typed_parameters.normalizers import *

class InnerStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="int",
		                 description="Value between 0 and 10",
		                 range=[0,10]),
		FloatParameter(name="optional_float",
		               default=None,
		               description="A float value, but that can be empty")
	]

	__DESCRIPTION__ = "A struct that will be owned by another one"

class Choices(enum.Enum):
	A=0
	B=1
	C=2

class MyStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="int", description="This is an int"),
		IntegerParameter(name="ranged_int", range=[0,10], description="Int value between 0 and 10"),
		IntegerParameter(name="odd_int", normalizer=ODD_NORMALIZER, description="Odd-only int"),
		StringParameter(name="str", description="Enter the text you want here"),
		StringParameter(name="str_with_default", default="lol", description="Your favorite laughing expression"),
		EnumParameter(name="enum_from_enum", choices=Choices, description="Be sure to make the right choice"),
		VectorParameter(type=int, name="optional_vector_int", description="The ages of your children"),
		StructParameter(type=InnerStruct, name="struct", description="A struct in the struct"),
	]

	__DESCRIPTION__="A Struct to demonstrate how auto documentation works"