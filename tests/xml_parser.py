import unittest
from masher.xml_parsing import XParser
from masher.xml_rules import ConstantRule
from masher.xml_rules import RandomRule
from masher.xml_rules import FileListRule
from masher.xml_rules import ListRule
from masher.xml_rules import PhraseRule

class ParserTest(unittest.TestCase):

    def setUp(self):
        p = XParser()
        p.add_rule(ConstantRule())
        p.add_rule(RandomRule(p))
        p.add_rule(FileListRule())
        p.add_rule(ListRule())
        p.add_rule(PhraseRule(p))
        self.parser = p

    def tearDown(self):
        pass

    def testOne(self):
        xml = """<?xml version="1.0"?>
        <list> hello; goodbye; </list>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual(["hello", "goodye"], gen.words)


if __name__ == "__main__":
    unittest.main()