from nineml.exceptions import NineMLSerializationNotSupportedError
from . import NINEML_BASE_NS
from collections import OrderedDict
from .base import BaseSerializer, BaseUnserializer, BODY_ATTR, NS_ATTR
from nineml.exceptions import (
    NineMLMissingSerializationError, NineMLNameError, NineMLSerializationError)


class DictSerializer(BaseSerializer):
    """
    A Serializer class that serializes to a dictionary of lists and attributes.
    Is used as the base class for the Pickle, JSON and YAML serializers
    """

    def create_elem(self, name, parent, namespace=None, multiple=False,  # @UnusedVariable @IgnorePep8
                    **options):  # @UnusedVariable
        elem = OrderedDict()
        if multiple:
            if name not in parent:
                parent[name] = []
            parent[name].append(elem)
        else:
            if name in parent:
                raise NineMLSerializationError(
                    "'{}' already exists in parent ({}) when creating "
                    "singleton element".format(name, parent))
            parent[name] = elem
        if namespace is not None:
            self.set_attr(elem, NS_ATTR, namespace, **options)
        return elem

    def create_root(self, **options):  # @UnusedVariable
        return OrderedDict()

    def set_attr(self, serial_elem, name, value, **options):  # @UnusedVariable
        serial_elem[name] = value

    def set_body(self, serial_elem, value, sole=False, **options):  # @UnusedVariable @IgnorePep8
        self.set_attr(serial_elem, BODY_ATTR, value, **options)

    def to_file(self, serial_elem, file, **options):  # @UnusedVariable  @IgnorePep8 @ReservedAssignment
        raise NineMLSerializationNotSupportedError(
            "'dict' format cannot be written to file"
            "(use JSON or Pickle)")

    def to_str(self, serial_elem, **options):  # @UnusedVariable  @IgnorePep8
        raise NineMLSerializationNotSupportedError(
            "'dict' format cannot be converted to a string "
            "(use JSON or Pickle)")


class DictUnserializer(BaseUnserializer):
    """
    A Unserializer class that unserializes from a dictionary of lists and
    attributes. Is used as the base class for the Pickle, JSON and YAML
    unserializers
    """

    def __init__(self, root, version, **kwargs):
        super(DictUnserializer, self).__init__(root, version, **kwargs)

    def get_child(self, parent, nineml_type, **options):  # @UnusedVariable
        try:
            child = parent[nineml_type]
        except KeyError:
            raise NineMLMissingSerializationError(
                "Missing '{}' in parent {}".format(nineml_type, parent))
        if not isinstance(child, dict):
            raise NineMLSerializationError(
                "Muliple children of type '{}' found in {}"
                .format(nineml_type, parent))

    def get_children(self, parent, nineml_type, **options):  # @UnusedVariable
        try:
            children = parent[nineml_type]
        except KeyError:
            children = []
        if not isinstance(children, list):
            raise NineMLSerializationError(
                "Single child of type '{}' found in {}"
                .format(nineml_type, parent))
        return iter(children)

    def get_attr(self, serial_elem, name, **options):  # @UnusedVariable
        try:
            value = serial_elem[name]
        except KeyError:
            raise NineMLNameError(
                "Element {} doesn't contain an '{}' attribute"
                .format(serial_elem, name))
        except TypeError:
            raise
        if self._is_child(value):
            raise NineMLNameError(
                "Element {} contains a '{}' child ({}) not an attribute"
                .format(serial_elem, name, value))
        return value

    def get_body(self, serial_elem, sole=True, **options):  # @UnusedVariable
        try:
            body = self.get_attr(serial_elem, BODY_ATTR)
        except NineMLNameError:
            body = None
        return body

    def get_attr_keys(self, serial_elem, **options):  # @UnusedVariable
        return (n for n, e in serial_elem.iteritems()
                if not self._is_child(e) and n not in (BODY_ATTR, NS_ATTR))

    def get_namespace(self, serial_elem, **options):  # @UnusedVariable
        try:
            ns = self.get_attr(serial_elem, NS_ATTR, **options)
        except NineMLNameError:
            ns = NINEML_BASE_NS + self.version
        return ns

    def from_file(self, file, **options):  # @ReservedAssignment
        raise NineMLSerializationNotSupportedError(
            "'dict' format cannot be read from a file"
            "(use JSON or Pickle)")

    def from_str(self, string, **options):
        raise NineMLSerializationNotSupportedError(
            "'dict' format cannot be read from a string "
            "(use JSON or Pickle)")

    @classmethod
    def _is_child(cls, elem):
        return isinstance(elem, (dict, list))