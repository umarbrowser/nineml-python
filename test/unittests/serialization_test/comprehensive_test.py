import shutil
import os.path
import tempfile
from unittest import TestCase
import nineml
from nineml.utils.testing.comprehensive import (
    instances_of_all_types, v1_safe_docs)
from nineml.serialization import ext_to_format, format_to_serializer


format_to_ext = dict((v, k) for k, v in ext_to_format.iteritems())  # @UndefinedVariable @IgnorePep8


class TestComprehensiveXML(TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_write_read_roundtrip(self):
        for version in (1.0, 2.0):
            if version == 1.0:
                docs = v1_safe_docs
            else:
                docs = instances_of_all_types['NineML'].values()
            for format in format_to_serializer:  # @ReservedAssignment
                try:
                    ext = format_to_ext[format]
                except KeyError:
                    continue  # ones that can't be written to file (e.g. dict)
                for i, document in enumerate(docs):
                    doc = document.clone()
                    url = os.path.join(
                        self._tmp_dir, 'test{}v{}.{}'.format(i, version, ext))
                    nineml.write(url, doc, format=format, version=version)
                    if format in ('yaml', 'json'):
                        with open(url) as f:
                            d = f.read()
                        print d
                    reread_doc = nineml.read(url, force_reload=True)
                    self.assertTrue(doc.equals(reread_doc),
                                    doc.find_mismatch(reread_doc))