# -*- coding: utf-8 -*-

# Standard libraries
import unittest

# strong_typing
from strong_typing.typed_containers import TypedList

class TypedListCreationTest(unittest.TestCase):

	def test_default(self):
		a = TypedList(int)

	def test_parameters(self):
		a = TypedList(int, [0,1])

	def test_bad_parameters(self):
		a = TypedList(int, ["0",1])
		with self.assertRaises(TypeError):
			a = TypedList(int, ["a",1])

class TypedListManipulationTest(unittest.TestCase):

	def setUp(self):
		self.list = TypedList(int)

	def test_typename(self):
		assert(self.list.typename == int)

	def test_addition(self):
		assert(len(self.list)) == 0
		self.list.appendDefault()
		self.list.extend([0,1.1])
		self.list.insert(1,10)
		self.list[4:] = [100, 20, "15"]
		self.list[4] = 17
		self.list.append("15")
		assert(len(self.list)) == 8
		assert(self.list == [0,10,0,1, 17, 20, 15, 15])
		assert(self.list != 0) # not a list
		assert(self.list != TypedList(float, [0, 10, 0, 1, 17, 20, 15, 15])) # different type
		assert(self.list != TypedList(int, [0, 10, 0, 1, 17, 20, 15])) # different length
		assert(self.list != TypedList(int, [0, 10, 0, 1, 17, 20, 15, 1])) # different content

	def test_no_addition(self):
		assert(len(self.list)) == 0
		self.list.append(0)
		with self.assertRaises(TypeError):
			self.list.append("a")
		with self.assertRaises(TypeError):
			self.list.extend([0, "a"])
		with self.assertRaises(TypeError):
			self.list.insert(0,"toto")
		with self.assertRaises(TypeError):
			self.list[0:] = [100, 20, "aq"]
		with self.assertRaises(TypeError):
			self.list[0] = "s"
		assert(len(self.list)) == 1

	def test_set_values(self):
		self.list.appendDefault()
		self.list[0] = "15"
		assert(self.list == [15])
		self.list[0] = 1
		assert(self.list == [1])
		self.list[0] = 2.0
		assert(self.list == [2])
		with self.assertRaises(TypeError):
			self.list[0] = dict(a=2.0)
		with self.assertRaises(TypeError):
			self.list[0] = [1,2]
		self.list.appendDefault()
		self.list.appendDefault()
		self.list[0:3:2] = [1, 2]
		assert(self.list == [1, 0, 2])

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
