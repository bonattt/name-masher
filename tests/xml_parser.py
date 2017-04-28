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
        p.add_rule(FileListRule())
        p.add_rule(ListRule())
        p.add_rule(RandomRule(p))
        p.add_rule(PhraseRule(p))
        self.parser = p

    def tearDown(self):
        pass

    def testListRule(self):
        xml = """<?xml version="1.0"?>
        <list>hello;goodbye;</list>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual(["hello", "goodbye"], gen.words)

    def testConstantRule(self):
        xml = """<?xml version="1.0"?>
        <const>hello</const>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual("hello", gen.word)

    def testFileListRule(self):
        xml = """<?xml version="1.0"?>
        <listfile>./test_files/test_names1.txt; ./test_files/test_names2.txt</listfile>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual(["name1","name2","name3","name4","name5","name6"], gen.words)

    def testRandomRule(self):
        xml = """<?xml version="1.0"?>
        <random><const>hello</const> <const> goodbye </const> </random>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual("hello", gen.generator.word)
        self.assertEqual("hello", gen.alt.word)

    def testPhraseRule(self):
        xml = """<?xml version="1.0"?>
        <phrase><const>hello</const> <const> goodbye </const> </phrase>"""
        gen = self.parser.parse_schema(xml)
        self.assertEqual(2, len(gen.generators))
        self.assertEqual("hello", gen.generators[0].word)
        self.assertEqual("goodbye", gen.generators[1].word)


class NewlineTest(unittest.TestCase):

    def setUp(self):
        xml = """<?xml version="1.0"?> <br/>"""
        self.gen = self.parser.parse_schema(xml)
        self.text = self.gen.generateText()

    def testTextGenerated(self):
        self.assertEqual("\n", self.text)


if __name__ == "__main__":
    unittest.main()