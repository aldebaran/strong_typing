# -*- coding: utf-8 -*-

# Standard libraries
import sys

# Third-party libraries
import enum
import collections
try:
	from python_qt_binding import QtGui, QtCore
	_qt_available = True
except ImportError:
	_qt_available = False

# Local modules
from ._struct import Struct
from .typed_containers import TypedList

# Check for Python version

if sys.version_info >= (3,0):
    unicode = str
    basestring = (str,bytes)
    long = int

if _qt_available:
	class ObjectDisplayWidget(QtGui.QTreeWidget):
		"""
		Tree widget displaying an object and giving the possibility to
		modify it.
		"""

		# ───────────
		# Constructor

		def __init__(self, parent=None, read_only=False):
			"""
			ObjectDisplayWidget constructor

			:param parent:  Parent of this widget
			"""
			super(ObjectDisplayWidget, self).__init__(parent)

			# Take as much space as possible
			self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

			# Three columns (key, value, delete button)
			self.setColumnCount(3)

			# Do not display column headers
			self.setHeaderHidden(True)

			# Resize the columns when some items are opened / close
			self.itemExpanded.connect(lambda: self.resizeColumnToContents(0))
			self.itemCollapsed.connect(lambda: self.resizeColumnToContents(0))
			self._data = None
			self.read_only = read_only

		# ──────────
		# Properties

		def data():
			doc="Object being displayed in the GUI"
			def fget(self):
				return self._data

			def fset(self, data_object):
				"""
				Clears the tree view and displays the new data object

				:param data_object: message object to display in the treeview
				"""
				# TODO: Remember whether items were expanded or not before deleting
				if self._data:
					self.clear()
					self._data = None

				if data_object:
					self._data = data_object
					# Populate the tree
					self._refresh_view()
				self.resizeColumnToContents(0)
				self.update()

			def fdel(self):
				if self._data:
					self.clear()
					self._data = None
					self.resizeColumnToContents(0)
					self.update()

			return locals()

		data = property(**data())

		@property
		def read_only(self):
			return self._read_only

		@read_only.setter
		def read_only(self, new_read_only_setting):
			self._read_only = new_read_only_setting

		# ────────────────
		# Internal methods

		def _refresh_view(self):
			# Call recursive function that will display each object level
			self._display_sub_items(parent_item=None,
			                        parent_obj=None,
			                        key= '',
			                        obj= self.data)

		def _display_sub_items(self, parent_item, parent_obj, key, obj):
			# Value to display at this level (if obj is not a container)
			value = None

			# Sub-objects contained in the current object (if obj is a container)
			subobjs = []

			if isinstance(obj, collections.Mapping):
				# obj is a container with keys  => retrieve its content to be displayed as sub-elements
				subobjs = obj.items()

			elif isinstance(obj, (collections.Sequence,collections.Set))\
			     and not isinstance(obj, basestring):
				# obj is a container  without keys => retrieve its content to be displayed as sub-elements by numbers
				# Give those sub-elements a number as name (like "[42]")
				if len(obj) != 0:
					subobjs = [(i, subobj) for (i, subobj) in enumerate(obj)]
			else:
				# obj is a plain value  => display it
				if isinstance(obj, float):
					value = '%.2f' % obj
				elif isinstance(obj, (basestring, bool, int, long)):
					value = str(obj)
				elif isinstance(obj, enum.Enum):
					value = obj.name
				elif obj is None:
					# typed containers cannot be "None", so any None is a value
					# User might want it to become a non-typed list but there is
					# no way to know it. So we'll assume is is supposed to be an editable
					# value
					value = ""
				else:
					print("Warning, unsupported type %s"%type(obj))

			## Create item
			if key != '':
				item = QtGui.QTreeWidgetItem()

				if parent_item is None:
					# This obj is a child of the root object
					self.addTopLevelItem(item)
				else:
					parent_item.addChild(item)

				# First column
				if isinstance(parent_obj, TypedList):
					item.setText(0, '['+str(key)+']') # Set name in first column
				else:
					item.setText(0, str(key)) # Set name in first column

				# Second column
				if value is not None:
					# obj is not a container, a value can be displayed
					if isinstance(obj, enum.Enum):
						# Enum is a limited set of choice
						# Display a ComboBox
						inputWidget = QtGui.QComboBox(self)
						for element in list(type(obj)):
							inputWidget.addItem(element.name)
							if element.name == value:
								# Ugly solution to set the default value, but unfortunately
								# QComboBox does not provide a way to set a value by text
								# without being editable
								inputWidget.setCurrentIndex(inputWidget.count()-1)
						inputWidget.currentIndexChanged[str].connect(lambda x: self._onValueChanged(parent_obj, item, key, x))
					else:
						# Other types are manually editable
						# Display a LineEdit
						inputWidget = QtGui.QLineEdit(self)
						inputWidget.setText(value)
						inputWidget.editingFinished.connect(lambda: self._refreshTextItem(parent_obj, item, key))
						## TODO ?? Use a QValidator to prevent Exceptions ?

				elif isinstance(obj, TypedList):
					# obj is a list, add a button to add elements
					inputWidget = QtGui.QPushButton(self)
					inputWidget.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
					inputWidget.setText("Add element")
					inputWidget.clicked.connect(lambda: self._elementAdditionRequired(item, obj))

				else:
					# obj can be
					# - a container without specified type
					# - a dict
					# - any unsupported type
					# on which addition is not supported
					inputWidget = None

				if inputWidget:
					self.setItemWidget(item, 1, inputWidget)
					inputWidget.setEnabled(not self._read_only)

				# Third column
				if isinstance(parent_obj, TypedList):
					# obj is an element of a container that supports removal
					inputWidget = QtGui.QPushButton(self)
					inputWidget.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
					inputWidget.setText("Remove element")
					inputWidget.clicked.connect(lambda: self._elementDeletionRequired(parent_item, parent_obj, item, key))
					self.setItemWidget(item, 2, inputWidget)
					inputWidget.setEnabled(not self._read_only)

			else:
				# Empty name means obj is the root => do nothing
				item = None

			# Add sub-elements if any
			for subobj_key, subobj in subobjs:
				self._display_sub_items(item, obj, subobj_key, subobj)

		def _onValueChanged(self, parent_obj, item, key, newvalue):
			setattr(parent_obj, key, newvalue)

		def _refreshTextItem(self, parent_obj, item, key):
			line_edit = self.itemWidget(item, 1)
			if line_edit is None:
				# This can happen when a lineEdit within a list is removed..
				return
			pal = line_edit.palette()
			try:
				if isinstance(parent_obj, (dict, list, set, tuple)):
					# Save the new value in object if possible
					parent_obj[key] = line_edit.text()
					# Retrieve the newly stored value
					# (it might be different from the input)
					new_value = str(parent_obj[key]) if parent_obj[key] is not None else ""
				else:
					setattr(parent_obj, key, line_edit.text())
					new_value = str(getattr(parent_obj, key)) if getattr(parent_obj, key) is not None else ""
				line_edit.setText(new_value)
			except ValueError:
				pal.setColor(QtGui.QPalette.Text, QtCore.Qt.red)
			else:
				pal.setColor(QtGui.QPalette.Text, self.palette().color(QtGui.QPalette.Text))
			line_edit.setPalette(pal)

		def _elementAdditionRequired(self, item, obj):
			# Add a new object to the list
			obj.appendDefault()

			# Display this new object in its container's widgetitem
			added_element_index = len(obj)-1
			self._display_sub_items(item, obj, added_element_index, obj[-1])

		def _elementDeletionRequired(self, parent_item, parent_obj, item, key):
			parent_item.removeChild(item) # Remove object displaying widget
			parent_item.takeChildren()
			parent_obj.pop(key) # Remove object from the container
			for (key, obj) in enumerate(parent_obj):
				self._display_sub_items(parent_item, parent_obj, key, obj)

	__all__=["ObjectDisplayWidget"]

else:
	__all__=[]