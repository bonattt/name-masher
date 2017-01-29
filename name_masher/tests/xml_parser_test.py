import unittest

from name_masher.xml_parser.parser import MasherXmlParser


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.parser = MasherXmlParser()

    def tearDown(self):
        pass

    def test_printing(self):
        self.parser.enable_debug_printing()
        self.parser.parse_file('../schemas/sword.xml')

    def test_set_end_char(self):
        xml = '<data endChar="3"> </data>'
        self.parser.parse_schema(xml)
        self.assertEqual("3", self.parser.end_char)

    def test_set_separator(self):
        xml = '<data separator=" "> </data>'
        self.parser.parse_schema(xml)
        self.assertEqual(" ", self.parser.separator)


if __name__ == "__main__":
    print("xml_parser_test.py")
    unittest.main()