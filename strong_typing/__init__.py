# -*- coding: utf-8 -*-

def load_doc():
	import os
	return open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../README.rst')).read()

def load_version():
	import os
	CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
	return open(os.path.join(CONTAINING_DIRECTORY,"VERSION")).read().split()[0]

__doc__ = load_doc()
__VERSION__ = load_version()

from . import typed_parameters
from . import typed_containers

from ._struct import *
from ._versioned_struct import *
from ._display_widget import *

# Remove symbols that must not be exported
del load_doc
del load_version

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
