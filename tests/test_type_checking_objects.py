# -*- coding: utf-8 -*-

# Standard libraries
import unittest

# Third-party libraries
import enum

# strong_typing
from strong_typing import Struct
from strong_typing.typed_containers import TypedList
from strong_typing.typed_parameters import *

class TypeCheckingNumericTest(unittest.TestCase):

	def setUp(self):
		class TestStruct(Struct):
			__ATTRIBUTES__= [
				IntegerParameter(name="int"),
				IntegerParameter(name="ranged_int", range=["0","10"]),
				IntegerParameter(name="odd_int", normalizer=ODD_NORMALIZER),
				IntegerParameter(name="optional_int", default=None),
				FloatParameter(name="float"),
				FloatParameter(name="ranged_float", range=[1,10]),
				FloatParameter(name="optional_float", default=None)
			]

		self.instance = TestStruct()


	def test_default_value(self):
		assert(self.instance.int == 0)
		assert(self.instance.ranged_int == 0)
		assert(self.instance.odd_int == 1)
		assert(self.instance.optional_int == None)
		assert(self.instance.float == 0.0)
		assert(self.instance.ranged_float == 1.0)
		assert(self.instance.optional_float == None)

	def test_set_value(self):
		self.instance.int = 100
		self.instance.ranged_int = 100
		self.instance.odd_int = 100
		self.instance.optional_int = 100
		self.instance.float = 100
		self.instance.ranged_float = 100
		self.instance.optional_float = 100

		assert(self.instance.int == 100)
		assert(self.instance.ranged_int == 10)
		assert(self.instance.odd_int == 101)
		assert(self.instance.optional_int == 100)
		assert(self.instance.float == 100.0)
		assert(self.instance.ranged_float == 10.0)
		assert(self.instance.optional_float == 100.0)

	def test_del_value(self):
		# Set some values
		self.instance.int = 100
		self.instance.ranged_int = 100
		self.instance.odd_int = 100
		self.instance.optional_int = 100
		self.instance.float = 100
		self.instance.ranged_float = 100
		self.instance.optional_float = 100

		# Unset them
		self.instance.int = None
		self.instance.ranged_int = None
		self.instance.odd_int = None
		self.instance.optional_int = None
		self.instance.float = None
		self.instance.ranged_float = ""
		self.instance.optional_float = None

		# Check parameters are back to default value
		assert(self.instance.int == 0)
		assert(self.instance.ranged_int == 0)
		assert(self.instance.odd_int == 1)
		assert(self.instance.optional_int == None)
		assert(self.instance.float == 0.0)
		assert(self.instance.ranged_float == 1.0)
		assert(self.instance.optional_float == None)

		## AGAIN, with ``del``

		# Set some values
		self.instance.int = 100
		self.instance.ranged_int = 100
		self.instance.odd_int = 100
		self.instance.optional_int = 100
		self.instance.float = 100
		self.instance.ranged_float = 100
		self.instance.optional_float = 100

		# Unset them
		del self.instance.int
		del self.instance.ranged_int
		del self.instance.odd_int
		del self.instance.optional_int
		del self.instance.float
		del self.instance.ranged_float
		del self.instance.optional_float

		# Check parameters are back to default value
		assert(self.instance.int == 0)
		assert(self.instance.ranged_int == 0)
		assert(self.instance.odd_int == 1)
		assert(self.instance.optional_int == None)
		assert(self.instance.float == 0.0)
		assert(self.instance.ranged_float == 1.0)
		assert(self.instance.optional_float == None)

class TypeCheckingBoolTest(unittest.TestCase):
	def setUp(self):
		class TestStruct(Struct):
			__ATTRIBUTES__= [
				BoolParameter(name="bool"),
				BoolParameter(name="optional_bool", default=None),
			]

		self.instance = TestStruct()

	def test_default_value(self):
		assert(self.instance.bool == False)
		assert(self.instance.optional_bool == None)

	def test_set_value(self):
		self.instance.bool = True
		self.instance.optional_bool = "true"
		assert(self.instance.bool == True)
		assert(self.instance.optional_bool == True)

		self.instance.bool = "0"
		self.instance.optional_bool = "false"
		assert(self.instance.bool == False)
		assert(self.instance.optional_bool == False)

	def test_del_value(self):
		# Set some values
		self.instance.bool = True
		self.instance.optional_bool = True

		# Unset them
		self.instance.bool = None
		self.instance.optional_bool = None

		# Check parameters are back to default value
		assert(self.instance.bool == False)
		assert(self.instance.optional_bool == None)

		## AGAIN, with ``del``

		# Set some values
		self.instance.bool = True
		self.instance.optional_bool = True

		# Unset them
		del self.instance.bool
		del self.instance.optional_bool

		# Check parameters are back to default value
		assert(self.instance.bool == False)
		assert(self.instance.optional_bool == None)

class TypeCheckingStringTest(unittest.TestCase):
	def setUp(self):
		class TestStruct(Struct):
			__ATTRIBUTES__= [
				StringParameter(name="str"),
				StringParameter(name="optional_str", default=None),
			]

		self.instance = TestStruct()

	def test_default_value(self):
		assert(self.instance.str == "")
		assert(self.instance.optional_str == "")

	def test_set_value(self):
		self.instance.str = "Toto"
		self.instance.optional_str = 0
		assert(self.instance.str == "Toto")
		assert(self.instance.optional_str == "0")

	def test_del_value(self):
		# Set some values
		self.instance.str = 100
		self.instance.optional_str = 10

		# Unset them
		self.instance.str = None
		self.instance.optional_str = None

		# Check parameters are back to default value
		assert(self.instance.str == "")
		assert(self.instance.optional_str == "")

		## AGAIN, with ``del``

		# Set some values
		self.instance.str = "a"
		self.instance.optional_str = "b"

		# Unset them
		del self.instance.str
		del self.instance.optional_str

		# Check parameters are back to default value
		assert(self.instance.str == "")
		assert(self.instance.optional_str == "")

class TypeCheckingEnumTest(unittest.TestCase):
	class Choices(enum.Enum):
			A=0
			B=1
			C=2

	def setUp(self):
		class TestStruct(Struct):
			__ATTRIBUTES__= [
				EnumParameter(name="enum_from_list", choices=["a", "b", "c"]),
				EnumParameter(name="enum_from_list_with_default", choices=["a", "b", "c"], default="b"),
				EnumParameter(name="enum_from_enum", choices=TypeCheckingEnumTest.Choices),
				EnumParameter(name="enum_from_enum_with_default", choices=TypeCheckingEnumTest.Choices, default=TypeCheckingEnumTest.Choices.B),
				EnumParameter(name="enum_from_enum_with_default2", choices=TypeCheckingEnumTest.Choices, default="B"),
			]

		self.instance = TestStruct()

	def test_default_value(self):
		assert(self.instance.enum_from_list == "a")
		assert(self.instance.enum_from_list_with_default == "b")
		assert(self.instance.enum_from_enum == TypeCheckingEnumTest.Choices.A)
		assert(self.instance.enum_from_enum_with_default == TypeCheckingEnumTest.Choices.B)
		assert(self.instance.enum_from_enum_with_default2 == TypeCheckingEnumTest.Choices.B)

	def test_set_value(self):
		self.instance.enum_from_list = "c"
		self.instance.enum_from_list_with_default = "c"
		self.instance.enum_from_enum = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default2 = TypeCheckingEnumTest.Choices.C

		assert(self.instance.enum_from_list == "c")
		assert(self.instance.enum_from_list_with_default == "c")
		assert(self.instance.enum_from_enum == TypeCheckingEnumTest.Choices.C)
		assert(self.instance.enum_from_enum_with_default == TypeCheckingEnumTest.Choices.C)
		assert(self.instance.enum_from_enum_with_default2 == TypeCheckingEnumTest.Choices.C)

	def test_del_value(self):
		# Set some values
		self.instance.enum_from_list = "c"
		self.instance.enum_from_list_with_default = "c"
		self.instance.enum_from_enum = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default2 = TypeCheckingEnumTest.Choices.C

		# Unset them
		self.instance.enum_from_list = None
		self.instance.enum_from_list_with_default = None
		self.instance.enum_from_enum = None
		self.instance.enum_from_enum_with_default = None
		self.instance.enum_from_enum_with_default2 = None

		# Check parameters are back to default value
		assert(self.instance.enum_from_list == "a")
		assert(self.instance.enum_from_list_with_default == "b")
		assert(self.instance.enum_from_list_with_default != 0)
		assert(self.instance.enum_from_enum == TypeCheckingEnumTest.Choices.A)
		assert(self.instance.enum_from_enum_with_default == TypeCheckingEnumTest.Choices.B)
		assert(self.instance.enum_from_enum_with_default2 == TypeCheckingEnumTest.Choices.B)

		## AGAIN, with ``del``

		# Set some values
		self.instance.enum_from_list = "c"
		self.instance.enum_from_list_with_default = "c"
		self.instance.enum_from_enum = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default = TypeCheckingEnumTest.Choices.C
		self.instance.enum_from_enum_with_default2 = TypeCheckingEnumTest.Choices.C

		# Unset them
		del self.instance.enum_from_list
		del self.instance.enum_from_list_with_default
		del self.instance.enum_from_enum
		del self.instance.enum_from_enum_with_default
		del self.instance.enum_from_enum_with_default2

		# Check parameters are back to default value
		assert(self.instance.enum_from_list == "a")
		assert(self.instance.enum_from_list_with_default == "b")
		assert(self.instance.enum_from_enum == TypeCheckingEnumTest.Choices.A)
		assert(self.instance.enum_from_enum_with_default == TypeCheckingEnumTest.Choices.B)
		assert(self.instance.enum_from_enum_with_default2 == TypeCheckingEnumTest.Choices.B)

	def test_failing_creation(self):
		with self.assertRaises(TypeError):
			EnumParameter("a,b,c,d", name="not_a_correct_enum_nor_list")

		with self.assertRaises(TypeError):
			EnumParameter([], name="empty_choice_list")

class TypeCheckingVectorTest(unittest.TestCase):

	def setUp(self):
		class TestStruct(Struct):
			## It is not possible yet to nest vectors..
			## It should be added in the future

			__ATTRIBUTES__= [
				VectorParameter(type=int, name="vector_int", default=[0]),
				# Vector(name="vector_vector_int"),
				VectorParameter(type=int, name="optional_vector_int"),
				# Vector(name="optional_vector_vector_int"),
			]

		self.instance = TestStruct()

	def test_default_value(self):
		assert(self.instance.vector_int == [0])
		assert(self.instance.optional_vector_int == [])

	def test_set_value(self):
		## No need to test everything, almost all important stuff are in
		## the specific test file for TypedList
		self.instance.vector_int = [1.0]
		self.instance.optional_vector_int = ["10", 10.0]
		assert(self.instance.vector_int == [1])
		assert(self.instance.optional_vector_int == [10, 10])

	def test_del_value(self):
		# Set some values
		self.instance.vector_int = [1.0]
		self.instance.optional_vector_int = ["10", 10.0]

		# Unset them
		self.instance.vector_int = None
		self.instance.optional_vector_int = None

		# Check parameters are back to default value
		assert(self.instance.vector_int == [0])
		assert(self.instance.optional_vector_int == [])

		## AGAIN, with ``del``

		# Set some values
		self.instance.vector_int = [1.0]
		self.instance.optional_vector_int = ["10", 10.0]

		# Unset them
		del self.instance.vector_int
		del self.instance.optional_vector_int

		# Check parameters are back to default value
		assert(self.instance.vector_int == [0])
		assert(self.instance.optional_vector_int == [])

	def test_failing_creation(self):
		with self.assertRaises(TypeError):
			VectorParameter(type=int, name="not_a_list as_default", default=10)


class TypeCheckingStructTest(unittest.TestCase):

	class InnerTestStruct(Struct):
			__ATTRIBUTES__= [
				IntegerParameter(name="ranged_int", range=[0,10]),
				FloatParameter(name="optional_float", default=None)
			]

	def setUp(self):

		class TestStruct(Struct):
			__ATTRIBUTES__= [
				StructParameter(type=TypeCheckingStructTest.InnerTestStruct, name="struct"),
				StructParameter(type=TypeCheckingStructTest.InnerTestStruct, name="struct_with_default", default=TypeCheckingStructTest.InnerTestStruct(5, 20.0)),
			]

		self.instance = TestStruct()

	def test_default_value(self):
		assert(self.instance.struct.ranged_int == 0)
		assert(self.instance.struct.optional_float == None)
		assert(self.instance.struct_with_default.ranged_int == 5)
		assert(self.instance.struct_with_default.optional_float == 20.0)

	def test_set_value(self):
		self.instance.struct = TypeCheckingStructTest.InnerTestStruct(15, 30)
		self.instance.struct_with_default =TypeCheckingStructTest. InnerTestStruct(-1)
		assert(self.instance.struct.ranged_int == 10)
		assert(self.instance.struct.optional_float == 30.0)
		assert(self.instance.struct_with_default.ranged_int == 0)
		assert(self.instance.struct_with_default.optional_float == None)

	def test_del_value(self):
		# Set some values
		self.instance.struct = TypeCheckingStructTest.InnerTestStruct(15, 30)
		self.instance.struct_with_default = TypeCheckingStructTest.InnerTestStruct(-1)

		# Unset them
		self.instance.struct = None
		self.instance.struct_with_default = None

		# Check parameters are back to default value
		assert(self.instance.struct.ranged_int == 0)
		assert(self.instance.struct.optional_float == None)
		assert(self.instance.struct_with_default.ranged_int == 5)
		assert(self.instance.struct_with_default.optional_float == 20.0)

		## AGAIN, with ``del``

		# Set some values
		self.instance.struct = TypeCheckingStructTest.InnerTestStruct(15, 30)
		self.instance.struct_with_default = TypeCheckingStructTest.InnerTestStruct(-1)

		# Unset them
		del self.instance.struct
		del self.instance.struct_with_default

		# Check parameters are back to default value
		assert(self.instance.struct.ranged_int == 0)
		assert(self.instance.struct.optional_float == None)
		assert(self.instance.struct_with_default.ranged_int == 5)
		assert(self.instance.struct_with_default.optional_float == 20.0)

	def test_default_value_stability(self):
		# Set struct's int value
		self.instance.struct_with_default.ranged_int = 10

		# Reset struct to the default
		self.instance.struct_with_default = None

		# Make sure the struct's int is back to the default
		assert(self.instance.struct_with_default.ranged_int == 5)

		## AGAIN !!

		# Set struct's int value
		self.instance.struct_with_default.ranged_int = 10

		# Reset struct to the default
		self.instance.struct_with_default = None

		# Make sure the struct's int is back to the default
		assert(self.instance.struct_with_default.ranged_int == 5)

	# def test_failing_creation(self):
	# 	with self.assertRaises(TypeError):
	# 		Vector(type=int, name="not_a_list as_default", default=10)
