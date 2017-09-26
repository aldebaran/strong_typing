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
import collections

# ─────────────────────
# Formatting parameters

def unicodeWithAsciiFallback(unicode_char, ascii_char, encoder=str):
	try:
		return encoder(unicode_char)
	except UnicodeEncodeError:
		return ascii_char

INDENT_SIZE = 3
AFTER_MID_INDENT= lambda x: unicodeWithAsciiFallback(u'│', '|', x) + ' ' * (INDENT_SIZE-1)
AFTER_LAST_INDENT=lambda x: ' ' * (INDENT_SIZE)
TREE_INDENT=lambda x: unicodeWithAsciiFallback(u'─', '-', x)*(INDENT_SIZE-2) + " "
TREE_MID_INDENT=lambda x: unicodeWithAsciiFallback(u'├', '|', x) + TREE_INDENT(x)
TREE_LAST_INDENT=lambda x: unicodeWithAsciiFallback(u'└', '|', x) + TREE_INDENT(x)

def textualize_mapping(mapping, display_type=str):
	"""
	Pretty print of mappings

	:param mapping: Mapping to display
	:param display_type: Output type ("str" or "unicode", "str" is default)
	"""
	return textualize(list(mapping.keys()), mapping, display_type)

def textualize_sequence(sequence, display_type=str):
	"""
	Pretty print of sequence

	:param sequence: Sequence to display
	:param display_type: Output type ("str" or "unicode", "str" is default)
	"""
	return textualize(range(len(sequence)), sequence, display_type)

def textualize(keys, map, display_type):
	res_str = ""
	for key in keys:
		value = map[key]
		value = value if value != "" else "\"\""
		if key != keys[-1]:
			res_str += "\n" + TREE_MID_INDENT(display_type)
			indent_level = AFTER_MID_INDENT(display_type)
		else:
			res_str += "\n" + TREE_LAST_INDENT(display_type)
			indent_level = AFTER_LAST_INDENT(display_type)
		res_str += display_type(key) + ": "
		res_str += display_type(value).replace("\n","\n"+(indent_level))
	return res_str

class TextualizeMixin(object):
	def __getitem__(self, key):
		raise NotImplementedError

	def __len__(self):
		raise NotImplementedError

	def __str__(self):
		return self._textualize(str)

	def __unicode__(self):
		return self._textualize(unicode)

	def _textualize(self, display_type):
		if isinstance(self, collections.Mapping):
			if len(self) == 0:
				return "{}"
			return textualize_mapping(self, display_type)
		elif isinstance(self, collections.Sequence):
			if len(self) == 0:
				return "[]"
			return textualize_sequence(self, display_type)
		else:
			raise Exception("Only collections.{Sequence,Mapping} are supported")

__all__=["TextualizeMixin"]