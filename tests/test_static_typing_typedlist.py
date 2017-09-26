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
from strong_typing.typed_containers import TypedList

def test_default():
	a = TypedList(int)

def test_parameters():
	a = TypedList(int, [0,1])

def test_bad_parameters():
	a = TypedList(int, ["0",1])
	with pytest.raises(TypeError):
		a = TypedList(int, ["a",1])

def test_typename():
	assert(TypedList(int).typename == int)

def test_addition():
	my_list = TypedList(int)
	assert(len(my_list)) == 0
	my_list.appendDefault()
	my_list.extend([0,1.1])
	my_list.insert(1,10)
	my_list[4:] = [100, 20, "15"]
	my_list[4] = 17
	my_list.append("15")
	assert(len(my_list)) == 8
	assert(my_list == [0,10,0,1, 17, 20, 15, 15])
	assert(my_list != 0) # not a list
	assert(my_list != TypedList(float, [0, 10, 0, 1, 17, 20, 15, 15])) # different type
	assert(my_list != TypedList(int, [0, 10, 0, 1, 17, 20, 15])) # different length
	assert(my_list != TypedList(int, [0, 10, 0, 1, 17, 20, 15, 1])) # different content

def test_no_addition():
	my_list = TypedList(int)
	assert(len(my_list)) == 0
	my_list.append(0)
	with pytest.raises(TypeError):
		my_list.append("a")
	with pytest.raises(TypeError):
		my_list.extend([0, "a"])
	with pytest.raises(TypeError):
		my_list.insert(0,"toto")
	with pytest.raises(TypeError):
		my_list[0:] = [100, 20, "aq"]
	with pytest.raises(TypeError):
		my_list[0] = "s"
	assert(len(my_list)) == 1

def test_set_values():
	my_list = TypedList(int)
	my_list.appendDefault()
	my_list[0] = "15"
	assert(my_list == [15])
	my_list[0] = 1
	assert(my_list == [1])
	my_list[0] = 2.0
	assert(my_list == [2])
	with pytest.raises(TypeError):
		my_list[0] = dict(a=2.0)
	with pytest.raises(TypeError):
		my_list[0] = [1,2]
	my_list.appendDefault()
	my_list.appendDefault()
	my_list[0:3:2] = [1, 2]
	assert(my_list == [1, 0, 2])

# class MultipleTypedListManipulationTest(unittest.TestCase):

# 	def setUp(self):
# 		self.ilist = TypedList(int)()
# 		self.flist = TypedList(float)()

# 	def test_addition(self):
# 		self.ilist.append(0)
# 		self.flist.append(0.0)
# 		assert(type(self.ilist[0]) == int)
# 		assert(type(self.flist[0]) == float)
# 		assert(self.ilist != self.flist)

# class NestedTypedListManipulationTest(unittest.TestCase):

# 	def setUp(self):
# 		self.ilist = TypedList(TypedList(int))()
# 		self.flist = TypedList(int)()

# 	def test_addition(self):
# 		self.ilist.append(0)
# 		self.flist.append(0.0)
# 		assert(type(self.ilist[0]) == int)
# 		assert(type(self.flist[0]) == float)
# 		assert(self.ilist != self.flist)
