# -*- coding: utf-8 -*-

# Standard libraries
import unittest

# strong_typing
from strong_typing import Struct
from strong_typing.typed_parameters import *
from strong_typing.typed_parameters.normalizers import *

class StructCreationTest(unittest.TestCase):

	def test_default(self):
		a = Struct()

	def test_new_struct(self):
		class AStruct(Struct):
			__ATTRIBUTES__= [IntegerParameter(name="a", default=1)]

		instanceA = AStruct()
		assert(instanceA.a == 1)
		instanceB = AStruct(a=2)
		assert(instanceB.a == 2)
		instanceC = AStruct(4)
		assert(instanceC.a == 4)
		instanceA.a = 4

		with self.assertRaises(TypeError):
			AStruct(0, 1)
		with self.assertRaises(TypeError):
			AStruct(b=0)

		assert(instanceA == instanceC)
		assert(instanceA != instanceB)

		instanceD = AStruct(instanceA)
		assert(instanceA == instanceD)