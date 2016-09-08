import unittest
from nineml.utils.testing.comprehensive import (
    all_types, instances_of_all_types)


class TestAccessors(unittest.TestCase):

    def test_accessors(self):
        for name, cls in all_types.iteritems():
            if hasattr(cls, 'class_to_member'):
                for member in cls.class_to_member:
                    for elem in instances_of_all_types[name]:
                        self.assertIsInstance(
                            elem._num_members(member, cls.class_to_member),
                            int)


class TestRepr(unittest.TestCase):

    def test_repr(self):
        for name, elems in instances_of_all_types.iteritems():
            for elem in elems:
                if name == 'NineMLDocument':
                    self.assertTrue(repr(elem).startswith('Document'))
                else:
                    self.assertTrue(
                        repr(elem).startswith(name),
                        "__repr__ for {} instance does not start with '{}' ('{}')"
                        .format(name, all_types[name].__name__, repr(elem)))
