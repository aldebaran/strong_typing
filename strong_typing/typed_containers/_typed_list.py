# -*- coding: utf-8 -*-

# strong_typing
from .._textualize import TextualizeMixin
from .._struct import Struct

# class TypedList(type):

#     def __new__(mcs, typename):

class TypedList(list, TextualizeMixin):
    """
    Contains a list of statically-typed objects.
    """

    # ───────────
    # Constructor

    def __init__(self, typename, args=[]):
        """
        Create a TypedList

        :param typename: Type to be accepted in the list (type or class)
        :param args: List of initialization arguments (can be empty)
        :raises: TypeError if argument type is invalid
        """
        self.__typename = typename
        for element in args:
            self.append(element=element)

    # ───────
    # Methods

    def __setitem__(self, index, value):
        if isinstance(value, (list, set, tuple)) and isinstance(index, slice):
            list_to_extend = []
            for element in value:
                list_to_extend.append(self._checkType(element))
            list.__setitem__(self, index, list_to_extend)
        else:
            list.__setitem__(self, index, self._checkType(value))

    def __setslice__(self, start, stop, value):
        self.__setitem__(slice(start, stop), value)

    def _checkType(self, element):
        try:
            if isinstance(element, self.__typename):
                return element
            elif issubclass(self.__typename, Struct) and isinstance(element, dict):
                return self.__typename(**element)
            else:
                return self.__typename(element)
        except Exception, e:
            msg = "TypedList: list elements are expected to be %s. %s received"
            msg = msg%(self.__typename, type(element))
            raise TypeError(msg)

    def extend(self, iterable):
        list_to_extend = []
        for element in iterable:
            list_to_extend.append(self._checkType(element))

        list.extend(self, list_to_extend)

    def append(self, element):
        list.append(self, self._checkType(element))

    def insert(self, index, element):
        list.insert(self, index, self._checkType(element))

    def appendDefault(self):
        list.append(self, self.__typename())

    # ──────────
    # Properties

    @property
    def typename(self):
        return self.__typename

    # ─────────
    # Operators

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        elif isinstance(other, TypedList) and self.typename != other.typename:
            return False
        elif len(self) != len(other):
            return False
        else:
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
        return True

    def __ne__(self, other):
        return not (self == other)

        # return DefinedTypedList
        # return type('TypedList_'+typename.__name__, (DefinedTypedList,), dict())

__all__ = ["TypedList"]