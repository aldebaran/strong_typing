# -*- coding: utf-8 -*-

def load_doc():
	import os
	return open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../README.rst')).read()

def test_pyside_presence():
	try:
		import PySide
		return True
	except ImportError:
		return False

__doc__ = load_doc()

import typed_parameters
import typed_containers

from _struct import *
from _versioned_struct import *

if test_pyside_presence():
	from _display_widget import *

# Remove symbols that must not be exported
del load_doc
del test_pyside_presence

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
