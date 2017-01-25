# -*- coding: utf-8 -*-

# Standard libraries
import collections

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
			keys = self.keys()
			if len(keys) == 0:
				return "{}"
		elif isinstance(self, collections.Sequence):
			keys = range(len(self))
			if len(keys) == 0:
				return "[]"
		else:
			raise Exception("Only collections.{Sequence,Mapping} are supported")
		return textualize(keys, self, display_type)

__all__=["TextualizeMixin"]