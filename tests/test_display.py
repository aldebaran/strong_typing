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

# Standard libraries
import sys

# Third-party libraries
import enum
import pytest
try:
	from Qt import QtCore
	qt_available = True
	from strong_typing import ObjectDisplayWidget
except ImportError as e:
	print(e)
	qt_available = False

# Local modules
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

class SpecialTestStruct(Struct):
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

@pytest.mark.gui
def test_display(qtbot):
	instance = SpecialTestStruct()
	widget = ObjectDisplayWidget()
	widget.data = instance
	qtbot.addWidget(widget)
	widget.show()
	qtbot.waitForWindowShown(widget)

def test_textualize():
	instance = SpecialTestStruct()
	print(str(instance))
	if sys.version_info < (3, 0):
		print(unicode(instance))
