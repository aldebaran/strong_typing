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