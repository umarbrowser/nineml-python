from builtins import next
import unittest
from nineml.utils.comprehensive_example import instances_of_all_types
from nineml.exceptions import (NineMLXMLBlockError)


class TestRandomDistributionXMLLoaderExceptions(unittest.TestCase):

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_load_randomdistributionclass_ninemlxmlblockerror(self):
        """
        line #: 37
        message: Not expecting {} blocks within 'RandomDistribution' block

        context:
        --------
    def load_randomdistributionclass(self, element, **kwargs):
        xmlns = extract_xmlns(element.tag)
        if xmlns == NINEMLv1:
            lib_elem = expect_single(element.findall(NINEMLv1 +
                                                     'RandomDistribution'))
            if lib_elem.getchildren():
        """

        randomdistributionxmlloader = next(iter(instances_of_all_types['RandomDistributionXMLLoader'].values()))
        self.assertRaises(
            NineMLXMLBlockError,
            randomdistributionxmlloader.load_randomdistributionclass,
            element=None)

