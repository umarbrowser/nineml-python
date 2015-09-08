import os.path
import unittest
from nineml.user.port_connections import (AnalogPortConnection,
                                          EventPortConnection)


examples_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                            'xml', 'neurons')


class TestPortConnection(unittest.TestCase):

    def test_xml_roundtrip(self):
        pc1 = AnalogPortConnection('response', 'destination', 'iSyn', 'iExt')
        xml = pc1.to_xml()
        pc2 = AnalogPortConnection.from_xml(xml)
        self.assertEquals(pc1, pc2,
                          "XML round trip failed for AnalogPortConnection")
        pc1 = EventPortConnection('response', 'destination', 'iSyn', 'iExt')
        xml = pc1.to_xml()
        pc2 = AnalogPortConnection.from_xml(xml)
        self.assertEquals(pc1, pc2,
                          "XML round trip failed for AnalogPortConnection")