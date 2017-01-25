# -*- coding: utf-8 -*-

# Standard libraries
from collections import OrderedDict

# ─────────────────────
# Formatting parameters

INDENT_SIZE = 3
AFTER_MID_INDENT=lambda x: (u'│' if x is unicode else '|') + ' ' * (INDENT_SIZE-1)
AFTER_LAST_INDENT=lambda x: ' ' * (INDENT_SIZE)
TREE_INDENT=lambda x: (u'─' if x is unicode else '-')*(INDENT_SIZE-2) + " "
TREE_MID_INDENT=lambda x: (u'├' if x is unicode else '|') + TREE_INDENT(x)
TREE_LAST_INDENT=lambda x: (u'└' if x is unicode else '|') + TREE_INDENT(x)

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

class TextualizedList(list):
	def __str__(self):
		if len(self) == 0:
			return "[]"
		else:
			return textualize(range(len(self)), self, str)

	def __unicode__(self):
		if len(self) == 0:
			return "[]"
		else:
			return textualize(range(len(self)), self, unicode)

class TextualizedDict(OrderedDict):
	def __str__(self):
		if len(self.keys()) == 0:
			return "{}"
		else:
			return textualize(self.keys(), self, str)

	def __unicode__(self):
		if len(self.keys()) == 0:
			return "{}"
		else:
			# res_str = ""
			return textualize(self.keys(), self, unicode)

__all__=["TextualizedList", "TextualizedDict"]