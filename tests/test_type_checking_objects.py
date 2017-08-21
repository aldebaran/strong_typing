# -*- coding: utf-8 -*-

# Third-party libraries
import enum
import pytest

# strong_typing
from strong_typing import Struct
from strong_typing.typed_containers import TypedList
from strong_typing.typed_parameters import *
from strong_typing.typed_parameters.normalizers import *

class TypeCheckingNumericTestStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="int"),
		IntegerParameter(name="ranged_int", range=["0","10"]),
		IntegerParameter(name="odd_int", normalizer=ODD_NORMALIZER),
		IntegerParameter(name="optional_int", default=None),
		FloatParameter(name="float"),
		FloatParameter(name="ranged_float", range=[1,10]),
		FloatParameter(name="optional_float", default=None)
	]

class TypeCheckingBoolTestStruct(Struct):
	__ATTRIBUTES__= [
		BoolParameter(name="bool"),
		BoolParameter(name="optional_bool", default=None),
	]

class TypeCheckingStringTestStruct(Struct):
	__ATTRIBUTES__= [
		StringParameter(name="str"),
		StringParameter(name="optional_str", default=None),
	]

class Choices(enum.Enum):
	A=0
	B=1
	C=2

class TypeCheckingEnumTestStruct(Struct):
	__ATTRIBUTES__= [
		EnumParameter(name="enum_from_list", choices=["a", "b", "c"]),
		EnumParameter(name="enum_from_list_with_default", choices=["a", "b", "c"], default="b"),
		EnumParameter(name="enum_from_enum", choices=Choices),
		EnumParameter(name="enum_from_enum_with_default", choices=Choices, default=Choices.B),
		EnumParameter(name="enum_from_enum_with_default2", choices=Choices, default="B"),
	]

class TypeCheckingVectorTestStruct(Struct):
	## It is not possible yet to nest vectors..
	## It should be added in the future

	__ATTRIBUTES__= [
		VectorParameter(type=int, name="vector_int", default=[0]),
		# Vector(name="vector_vector_int"),
		VectorParameter(type=int, name="optional_vector_int"),
		# Vector(name="optional_vector_vector_int"),
	]

class InnerTestStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="ranged_int", range=[0,10]),
		FloatParameter(name="optional_float", default=None)
	]

class TypeCheckingStructTestStruct(Struct):
	__ATTRIBUTES__= [
		StructParameter(type=InnerTestStruct, name="struct"),
		StructParameter(type=InnerTestStruct, name="struct_with_default", default=InnerTestStruct(5, 20.0)),
	]

def test_numeric_default_value():
	instance = TypeCheckingNumericTestStruct()
	assert(instance.int == 0)
	assert(instance.ranged_int == 0)
	assert(instance.odd_int == 1)
	assert(instance.optional_int == None)
	assert(instance.float == 0.0)
	assert(instance.ranged_float == 1.0)
	assert(instance.optional_float == None)

def test_numeric_set_value():
	instance = TypeCheckingNumericTestStruct()
	instance.int = 100
	instance.ranged_int = 100
	instance.odd_int = 100
	instance.optional_int = 100
	instance.float = 100
	instance.ranged_float = 100
	instance.optional_float = 100

	assert(instance.int == 100)
	assert(instance.ranged_int == 10)
	assert(instance.odd_int == 101)
	assert(instance.optional_int == 100)
	assert(instance.float == 100.0)
	assert(instance.ranged_float == 10.0)
	assert(instance.optional_float == 100.0)

def test_numeric_del_value():
	instance = TypeCheckingNumericTestStruct()
	# Set some values
	instance.int = 100
	instance.ranged_int = 100
	instance.odd_int = 100
	instance.optional_int = 100
	instance.float = 100
	instance.ranged_float = 100
	instance.optional_float = 100

	# Unset them
	instance.int = None
	instance.ranged_int = None
	instance.odd_int = None
	instance.optional_int = None
	instance.float = None
	instance.ranged_float = ""
	instance.optional_float = None

	# Check parameters are back to default value
	assert(instance.int == 0)
	assert(instance.ranged_int == 0)
	assert(instance.odd_int == 1)
	assert(instance.optional_int == None)
	assert(instance.float == 0.0)
	assert(instance.ranged_float == 1.0)
	assert(instance.optional_float == None)

	## AGAIN, with ``del``

	# Set some values
	instance.int = 100
	instance.ranged_int = 100
	instance.odd_int = 100
	instance.optional_int = 100
	instance.float = 100
	instance.ranged_float = 100
	instance.optional_float = 100

	# Unset them
	del instance.int
	del instance.ranged_int
	del instance.odd_int
	del instance.optional_int
	del instance.float
	del instance.ranged_float
	del instance.optional_float

	# Check parameters are back to default value
	assert(instance.int == 0)
	assert(instance.ranged_int == 0)
	assert(instance.odd_int == 1)
	assert(instance.optional_int == None)
	assert(instance.float == 0.0)
	assert(instance.ranged_float == 1.0)
	assert(instance.optional_float == None)

def test_bool_default_value():
	instance = TypeCheckingBoolTestStruct()
	assert(instance.bool == False)
	assert(instance.optional_bool == None)

def test_bool_set_value():
	instance = TypeCheckingBoolTestStruct()
	instance.bool = True
	instance.optional_bool = "true"
	assert(instance.bool == True)
	assert(instance.optional_bool == True)

	instance.bool = "0"
	instance.optional_bool = "false"
	assert(instance.bool == False)
	assert(instance.optional_bool == False)

def test_bool_del_value():
	instance = TypeCheckingBoolTestStruct()

	# Set some values
	instance.bool = True
	instance.optional_bool = True

	# Unset them
	instance.bool = None
	instance.optional_bool = None

	# Check parameters are back to default value
	assert(instance.bool == False)
	assert(instance.optional_bool == None)

	## AGAIN, with ``del``

	# Set some values
	instance.bool = True
	instance.optional_bool = True

	# Unset them
	del instance.bool
	del instance.optional_bool

	# Check parameters are back to default value
	assert(instance.bool == False)
	assert(instance.optional_bool == None)

def test_string_default_value():
	instance = TypeCheckingStringTestStruct()
	assert(instance.str == "")
	assert(instance.optional_str == "")

def test_string_set_value():
	instance = TypeCheckingStringTestStruct()
	instance.str = "Toto"
	instance.optional_str = 0
	assert(instance.str == "Toto")
	assert(instance.optional_str == "0")

def test_string_del_value():
	instance = TypeCheckingStringTestStruct()
	# Set some values
	instance.str = 100
	instance.optional_str = 10

	# Unset them
	instance.str = None
	instance.optional_str = None

	# Check parameters are back to default value
	assert(instance.str == "")
	assert(instance.optional_str == "")

	## AGAIN, with ``del``

	# Set some values
	instance.str = "a"
	instance.optional_str = "b"

	# Unset them
	del instance.str
	del instance.optional_str

	# Check parameters are back to default value
	assert(instance.str == "")
	assert(instance.optional_str == "")

def test_enum_default_value():
	instance = TypeCheckingEnumTestStruct()
	assert(instance.enum_from_list == "a")
	assert(instance.enum_from_list_with_default == "b")
	assert(instance.enum_from_enum == Choices.A)
	assert(instance.enum_from_enum_with_default == Choices.B)
	assert(instance.enum_from_enum_with_default2 == Choices.B)

def test_enum_set_value():
	instance = TypeCheckingEnumTestStruct()
	instance.enum_from_list = "c"
	instance.enum_from_list_with_default = "c"
	instance.enum_from_enum = Choices.C
	instance.enum_from_enum_with_default = Choices.C
	instance.enum_from_enum_with_default2 = Choices.C

	assert(instance.enum_from_list == "c")
	assert(instance.enum_from_list_with_default == "c")
	assert(instance.enum_from_enum == Choices.C)
	assert(instance.enum_from_enum_with_default == Choices.C)
	assert(instance.enum_from_enum_with_default2 == Choices.C)

def test_enum_del_value():
	instance = TypeCheckingEnumTestStruct()

	# Set some values
	instance.enum_from_list = "c"
	instance.enum_from_list_with_default = "c"
	instance.enum_from_enum = Choices.C
	instance.enum_from_enum_with_default = Choices.C
	instance.enum_from_enum_with_default2 = Choices.C

	# Unset them
	instance.enum_from_list = None
	instance.enum_from_list_with_default = None
	instance.enum_from_enum = None
	instance.enum_from_enum_with_default = None
	instance.enum_from_enum_with_default2 = None

	# Check parameters are back to default value
	assert(instance.enum_from_list == "a")
	assert(instance.enum_from_list_with_default == "b")
	assert(instance.enum_from_list_with_default != 0)
	assert(instance.enum_from_enum == Choices.A)
	assert(instance.enum_from_enum_with_default == Choices.B)
	assert(instance.enum_from_enum_with_default2 == Choices.B)

	## AGAIN, with ``del``

	# Set some values
	instance.enum_from_list = "c"
	instance.enum_from_list_with_default = "c"
	instance.enum_from_enum = Choices.C
	instance.enum_from_enum_with_default = Choices.C
	instance.enum_from_enum_with_default2 = Choices.C

	# Unset them
	del instance.enum_from_list
	del instance.enum_from_list_with_default
	del instance.enum_from_enum
	del instance.enum_from_enum_with_default
	del instance.enum_from_enum_with_default2

	# Check parameters are back to default value
	assert(instance.enum_from_list == "a")
	assert(instance.enum_from_list_with_default == "b")
	assert(instance.enum_from_enum == Choices.A)
	assert(instance.enum_from_enum_with_default == Choices.B)
	assert(instance.enum_from_enum_with_default2 == Choices.B)

def test_enum_failing_creation():
	with pytest.raises(TypeError):
		EnumParameter("a,b,c,d", name="not_a_correct_enum_nor_list")

	with pytest.raises(TypeError):
		EnumParameter([], name="empty_choice_list")

def test_vector_default_value():
	instance = TypeCheckingVectorTestStruct()
	assert(instance.vector_int == [0])
	assert(instance.optional_vector_int == [])

def test_vector_set_value():
	instance = TypeCheckingVectorTestStruct()
	## No need to test everything, almost all important stuff are in
	## the specific test file for TypedList
	instance.vector_int = [1.0]
	instance.optional_vector_int = ["10", 10.0]
	assert(instance.vector_int == [1])
	assert(instance.optional_vector_int == [10, 10])

def test_vector_del_value():
	instance = TypeCheckingVectorTestStruct()
	# Set some values
	instance.vector_int = [1.0]
	instance.optional_vector_int = ["10", 10.0]

	# Unset them
	instance.vector_int = None
	instance.optional_vector_int = None

	# Check parameters are back to default value
	assert(instance.vector_int == [0])
	assert(instance.optional_vector_int == [])

	## AGAIN, with ``del``

	# Set some values
	instance.vector_int = [1.0]
	instance.optional_vector_int = ["10", 10.0]

	# Unset them
	del instance.vector_int
	del instance.optional_vector_int

	# Check parameters are back to default value
	assert(instance.vector_int == [0])
	assert(instance.optional_vector_int == [])

def test_vector_failing_creation():
	with pytest.raises(TypeError):
		VectorParameter(type=int, name="not_a_list as_default", default=10)

def test_struct_default_value():
	instance = TypeCheckingStructTestStruct()
	assert(instance.struct.ranged_int == 0)
	assert(instance.struct.optional_float == None)
	assert(instance.struct_with_default.ranged_int == 5)
	assert(instance.struct_with_default.optional_float == 20.0)

def test_struct_set_value():
	instance = TypeCheckingStructTestStruct()
	instance.struct = InnerTestStruct(15, 30)
	instance.struct_with_default = InnerTestStruct(-1)
	assert(instance.struct.ranged_int == 10)
	assert(instance.struct.optional_float == 30.0)
	assert(instance.struct_with_default.ranged_int == 0)
	assert(instance.struct_with_default.optional_float == None)

def test_struct_del_value():
	instance = TypeCheckingStructTestStruct()
	# Set some values
	instance.struct = InnerTestStruct(15, 30)
	instance.struct_with_default = InnerTestStruct(-1)

	# Unset them
	instance.struct = None
	instance.struct_with_default = None

	# Check parameters are back to default value
	assert(instance.struct.ranged_int == 0)
	assert(instance.struct.optional_float == None)
	assert(instance.struct_with_default.ranged_int == 5)
	assert(instance.struct_with_default.optional_float == 20.0)

	## AGAIN, with ``del``

	# Set some values
	instance.struct = InnerTestStruct(15, 30)
	instance.struct_with_default = InnerTestStruct(-1)

	# Unset them
	del instance.struct
	del instance.struct_with_default

	# Check parameters are back to default value
	assert(instance.struct.ranged_int == 0)
	assert(instance.struct.optional_float == None)
	assert(instance.struct_with_default.ranged_int == 5)
	assert(instance.struct_with_default.optional_float == 20.0)

def test_struct_default_value_stability():
	instance = TypeCheckingStructTestStruct()

	# Set struct's int value
	instance.struct_with_default.ranged_int = 10

	# Reset struct to the default
	instance.struct_with_default = None

	# Make sure the struct's int is back to the default
	assert(instance.struct_with_default.ranged_int == 5)

	## AGAIN !!

	# Set struct's int value
	instance.struct_with_default.ranged_int = 10

	# Reset struct to the default
	instance.struct_with_default = None

	# Make sure the struct's int is back to the default
	assert(instance.struct_with_default.ranged_int == 5)

# def test_failing_creation(self):
# 	with pytest.raises(TypeError):
# 		Vector(type=int, name="not_a_list as_default", default=10)
