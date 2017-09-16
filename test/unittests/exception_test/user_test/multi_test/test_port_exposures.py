from __future__ import print_function
from builtins import next
import unittest
from nineml.user.multi.port_exposures import (_BaseAnalogPortExposure, _LocalAnalogPortConnections, BasePortExposure)
from nineml.utils.comprehensive_example import instances_of_all_types
from nineml.exceptions import (NineMLImmutableError, NineMLRuntimeError)


class Test_BaseAnalogPortExposureExceptions(unittest.TestCase):

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_lhs_name_transform_inplace_ninemlimmutableerror(self):
        """
        line #: 158
        message: Cannot rename LHS of Alias '{}' because it is a analog port exposure

        context:
        --------
    def lhs_name_transform_inplace(self, name_map):
        """

        _baseanalogportexposure = next(iter(instances_of_all_types['_BaseAnalogPortExposure'].values()))
        self.assertRaises(
            NineMLImmutableError,
            _baseanalogportexposure.lhs_name_transform_inplace,
            name_map=None)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_set_dimension_ninemlimmutableerror(self):
        """
        line #: 167
        message: Cannot set dimension of port exposure (need to change the dimension of the referenced port).

        context:
        --------
    def set_dimension(self, dimension):
        """

        _baseanalogportexposure = next(iter(instances_of_all_types['_BaseAnalogPortExposure'].values()))
        self.assertRaises(
            NineMLImmutableError,
            _baseanalogportexposure.set_dimension,
            dimension=None)


class Test_LocalAnalogPortConnectionsExceptions(unittest.TestCase):

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_lhs_name_transform_inplace_ninemlimmutableerror(self):
        """
        line #: 306
        message: Cannot rename LHS of Alias '{}' because it is a local AnalogPortConnection

        context:
        --------
    def lhs_name_transform_inplace(self, name_map):
        """

        _localanalogportconnections = next(iter(instances_of_all_types['_LocalAnalogPortConnections'].values()))
        self.assertRaises(
            NineMLImmutableError,
            _localanalogportconnections.lhs_name_transform_inplace,
            name_map=None)


class TestBasePortExposureExceptions(unittest.TestCase):

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_sub_component_ninemlruntimeerror(self):
        """
        line #: 66
        message: Port exposure is not bound

        context:
        --------
    def sub_component(self):
        if self._sub_component is None:
        """

        baseportexposure = next(iter(instances_of_all_types['BasePortExposure'].values()))
        with self.assertRaises(NineMLRuntimeError):
            print(baseportexposure.sub_component)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_port_ninemlruntimeerror(self):
        """
        line #: 73
        message: Port exposure is not bound

        context:
        --------
    def port(self):
        if self._port is None:
        """

        baseportexposure = next(iter(instances_of_all_types['BasePortExposure'].values()))
        with self.assertRaises(NineMLRuntimeError):
            print(baseportexposure.port)

