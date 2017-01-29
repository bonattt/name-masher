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

    def test_constant_rule(self):
        xml = '<constant> hello </constant>'
        generators = self.parser.parse_schema(xml)
        self.assertEquals(1, len(generators))

    def test_list_rule(self):
        xml = ''
        generators = self.parser.parse_schema(xml)
        self.assertEquals(1, len(generators))

    def test_list_file_rule(self):
        xml = ''
        generators = self.parser.parse_schema(xml)
        self.assertEquals(1, len(generators))

    def test_random_rule(self):
        xml = ''
        generators = self.parser.parse_schema(xml)
        self.assertEquals(1, len(generators))

    def test_phrase_rule(self):
        xml = ''
        generators = self.parser.parse_schema(xml)
        self.assertEquals(1, len(generators))

    def test_rule_executes_on_all_tags(self):
        xml = ''
        self.parser.add_rule()
        generators = self.parser.parse_schema(xml)


class TagTallyRule:

    def __init__(self):
        self.tally = []

    def apply_rule(self, element, layer):
        self.tally.append(element.tag)


if __name__ == "__main__":
    print("xml_parser_test.py")
    unittest.main()