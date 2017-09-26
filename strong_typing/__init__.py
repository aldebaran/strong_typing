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


"""
**strong_typing** is a Python package containing some classes to create strongly
typed structures in Python

``strong_typing`` in a few words
--------------------------------

In Python, all variables are weakly typed, which means that a variable can take
all values of any type. The Python interpreter will then infer at runtime which
operations this variable can undergo depending on what it contains. This is
called "type inference".

This can be a problem in different situations

 - A function that does not receive the expected type as input
 - A variable or a class attribute whose type is changed through assignment

To avoid functions being called with bad arguments, you can use Python's
`typing module <https://docs.python.org/3/library/typing.html>`_) (however only
with Python3). To check if a variable is not incorrectly used, you can install
and run `mypy module <http://mypy.readthedocs.io/en/latest/>`_).

But if the latest is great for static check (without running the code), it does
not work on the code you don't own.

If, for instance you design a class expecting a certain type of attributes,
``mypy`` can very easily detect if you don't mistakenly override these
attributes with wrong typed data.

But if you put this class in a Python package and that someone else uses it,
there is no way to be sure they will respect your attribute's type.

To make sure they do, you would need to define a descriptor's class for each
attribute and define a setter function protecting your value against abusive
set. That's what we did :)

In the end, your class could look like this:

::

  class MyTypedStruct(Struct):
    __ATTRIBUTES__ = [IntegerParameter(name="my_int"),
                      FloatParameter(name="my_float")]
    __DESCRIPTION__ = "A sample of class with typed attributes"
"""

def load_version():
	import os
	CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
	return open(os.path.join(CONTAINING_DIRECTORY,"VERSION")).read().split()[0]

__VERSION__ = load_version()

from . import typed_parameters
from . import typed_containers

from ._struct import *
from ._versioned_struct import *
from ._display_widget import *

# Remove symbols that must not be exported
del load_version

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
