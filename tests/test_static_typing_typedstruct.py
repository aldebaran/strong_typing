# -*- coding: utf-8 -*-

# Third-party libraries
import pytest

# Local modules
from strong_typing import Struct
from strong_typing.typed_parameters import *
from strong_typing.typed_parameters.normalizers import *

def test_default():
	a = Struct()

def test_new_struct():
	class AStruct(Struct):
		__ATTRIBUTES__= [IntegerParameter(name="a", default=1)]

	instanceA = AStruct()
	assert(instanceA.a == 1)
	instanceB = AStruct(a=2)
	assert(instanceB.a == 2)
	instanceC = AStruct(4)
	assert(instanceC.a == 4)
	instanceA.a = 4

	with pytest.raises(TypeError):
		AStruct(0, 1)
	with pytest.raises(TypeError):
		a = AStruct(b=0)

	with pytest.raises(TypeError):
		a = AStruct()
		a["b"] = 2

	with pytest.raises(AttributeError):
		a = AStruct()
		a.b = 2

	assert(instanceA == instanceC)
	assert(instanceA != instanceB)

	instanceD = AStruct(instanceA)
	assert(instanceA == instanceD)