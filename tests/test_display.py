# -*- coding: utf-8 -*-

# Standard libraries
import unittest

# Third-party libraries
import enum
try:
	from PySide.QtGui import QApplication
	qt_available = True
except:
	qt_available = False

# strong_typing
from strong_typing import ObjectDisplayWidget
from strong_typing import Struct
from strong_typing.typed_parameters import *
from strong_typing.typed_parameters.normalizers import *

class InnerTestStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="int", range=[0,10]),
		FloatParameter(name="optional_float", default=None)
	]

class Choices(enum.Enum):
	A=0
	B=1
	C=2

class TestStruct(Struct):
	__ATTRIBUTES__= [
		IntegerParameter(name="int"),
		IntegerParameter(name="ranged_int", range=[0,10]),
		IntegerParameter(name="odd_int", normalizer=ODD_NORMALIZER),
		IntegerParameter(name="optional_int", default=None),
		FloatParameter(name="float"),
		BoolParameter(name="bool"),
		StringParameter(name="str"),
		StringParameter(name="str_with_default", default="lol"),
		EnumParameter(name="enum_from_list", choices=["a", "b", "c"]),
		EnumParameter(name="enum_from_list_with_default", choices=["a", "b", "c"], default="b"),
		EnumParameter(name="enum_from_enum", choices=Choices),
		EnumParameter(name="enum_from_enum_with_default", choices=Choices, default=Choices.B),
		EnumParameter(name="enum_from_enum_with_default2", choices=Choices, default="B"),
		VectorParameter(type=int, name="vector_int", default=[0]),
		VectorParameter(type=int, name="optional_vector_int"),
		StructParameter(type=InnerTestStruct, name="struct"),
		StructParameter(type=InnerTestStruct, name="struct_with_default", default=InnerTestStruct(5, 20.0)),
	]

if qt_available:
	class DisplayObjectTest(unittest.TestCase):

		def setUp(self):
			self.app = QApplication([])
			self.instance = TestStruct()

		def test_display(self):
			self.app.main_window = ObjectDisplayWidget()
			self.app.main_window.data = self.instance
			self.app.main_window.show()
			self.app.exec_()

class TextualizeObjectTest(unittest.TestCase):

	def setUp(self):
		self.instance = TestStruct()

	def test_textualize(self):
		print str(self.instance)
		print unicode(self.instance)

