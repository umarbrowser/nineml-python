import unittest
from nineml.user.selection import (Concatenate, find_difference, combined_port_accessor, combined_port_accessor)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLNameError)


class TestExceptions(unittest.TestCase):

    def test_find_difference_exception(self):
        """
        line #: 30
        message: errmsg

        context:
        --------
def find_difference(this, that):
    assert isinstance(that, this.__class__)
    if this != that:
        if isinstance(this, BaseULObject):
            for attr in this.defining_attributes:
                a = getattr(this, attr)
                b = getattr(that, attr)
                if a != b:
                    if attr in this.children:
                        find_difference(a, b)
                    else:
                        errmsg = ("'%s' attribute of %s instance '%s' differs:"
                                  " '%r' != '%r'" % (attr,
                                                     this.__class__.__name__,
                                                     this.name, a, b))
                        if type(a) != type(b):
                            errmsg += "(%s, %s)" % (type(a), type(b))
        """

        self.assertRaises(
            Exception,
            find_difference,
            this=None,
            that=None)

    def test_accessor_ninemlnameerror(self):
        """
        line #: 43
        message: '{}' {} is not present in all populations '{}' of the selection

        context:
        --------
def combined_port_accessor(population_accessor):
    def accessor(self, name):
        try:
            ports = [population_accessor(p, name) for p in self.populations]
        except NineMLNameError:
        """

        self.assertRaises(
            NineMLNameError,
            combined_port_accessor(population_accessor=None),
            name=None)

    def test_accessor_ninemlnameerror2(self):
        """
        line #: 50
        message: {} '{}' in populations '{}' are not equivalent

        context:
        --------
def combined_port_accessor(population_accessor):
    def accessor(self, name):
        try:
            ports = [population_accessor(p, name) for p in self.populations]
        except NineMLNameError:
            raise NineMLNameError(
                "'{}' {} is not present in all populations '{}' of the "
                "selection"
                .format(name, population_accessor.__name__,
                        "', '".join(p.name for p in self.populations)))
        port = ports[0]
        if any(p != port for p in ports):
        """

        self.assertRaises(
            NineMLNameError,
            combined_port_accessor(population_accessor=None),
            name=None)


class TestConcatenateExceptions(unittest.TestCase):

    def test_from_xml_valueerror(self):
        """
        line #: 261
        message: Duplicate indices found in Concatenate list ({})

        context:
        --------
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        items = []
        # Load references and indices from xml
        for it_elem in element.findall(extract_xmlns(element.tag) + 'Item'):
            items.append((
                get_xml_attr(it_elem, 'index', document, dtype=int, **kwargs),
                from_child_xml(it_elem, Population, document,
                               allow_reference='only', **kwargs)))
            try:
                kwargs['unprocessed'][0].discard(it_elem)
            except KeyError:
                pass
        # Sort by 'index' attribute
        indices, items = zip(*sorted(items, key=itemgetter(0)))
        indices = [int(i) for i in indices]
        if len(indices) != len(set(indices)):
        """

        self.assertRaises(
            ValueError,
            Concatenate.from_xml,
            element=None,
            document=None)

    def test_from_xml_valueerror2(self):
        """
        line #: 264
        message: Indices of Concatenate items must start from 0 ({})

        context:
        --------
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        items = []
        # Load references and indices from xml
        for it_elem in element.findall(extract_xmlns(element.tag) + 'Item'):
            items.append((
                get_xml_attr(it_elem, 'index', document, dtype=int, **kwargs),
                from_child_xml(it_elem, Population, document,
                               allow_reference='only', **kwargs)))
            try:
                kwargs['unprocessed'][0].discard(it_elem)
            except KeyError:
                pass
        # Sort by 'index' attribute
        indices, items = zip(*sorted(items, key=itemgetter(0)))
        indices = [int(i) for i in indices]
        if len(indices) != len(set(indices)):
            raise ValueError("Duplicate indices found in Concatenate list ({})"
                             .format(indices))
        if indices[0] != 0:
        """

        self.assertRaises(
            ValueError,
            Concatenate.from_xml,
            element=None,
            document=None)

    def test_from_xml_valueerror3(self):
        """
        line #: 267
        message: Missing indices in Concatenate items ({}), list must be contiguous.

        context:
        --------
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        items = []
        # Load references and indices from xml
        for it_elem in element.findall(extract_xmlns(element.tag) + 'Item'):
            items.append((
                get_xml_attr(it_elem, 'index', document, dtype=int, **kwargs),
                from_child_xml(it_elem, Population, document,
                               allow_reference='only', **kwargs)))
            try:
                kwargs['unprocessed'][0].discard(it_elem)
            except KeyError:
                pass
        # Sort by 'index' attribute
        indices, items = zip(*sorted(items, key=itemgetter(0)))
        indices = [int(i) for i in indices]
        if len(indices) != len(set(indices)):
            raise ValueError("Duplicate indices found in Concatenate list ({})"
                             .format(indices))
        if indices[0] != 0:
            raise ValueError("Indices of Concatenate items must start from 0 "
                             "({})".format(indices))
        if indices[-1] != len(indices) - 1:
        """

        self.assertRaises(
            ValueError,
            Concatenate.from_xml,
            element=None,
            document=None)
