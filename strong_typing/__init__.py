# -*- coding: utf-8 -*-

import os

__doc__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../README.rst')).read()

import typed_parameters
import typed_containers

try:
	import PySide
except ImportError:
	pass
else:
	from display_widget import ObjectDisplayWidget

from struct import Struct
from versioned_struct import VersionedStruct

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
