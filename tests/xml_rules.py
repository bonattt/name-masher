import unittest
from xml.etree import ElementTree
from masher import xml_rules
from masher.xml_rules import MasherXmlRuleError
from masher.generators import ConstantGenerator

def make_xml(xml):
    return '<?xml version="1.0"?><data>' + xml + '</data>'

class TestMisc(unittest.TestCase):

    def testCleanText(self):
        txt = xml_rules.clean_text_node('\n\thello\n\t')
        self.assertEqual('hello', txt)


class TextConstantRule(unittest.TestCase):

    def testMetBy(self):
        xml = '<const></const>'
        root = ElementTree.fromstring(xml)
        xml_rules.ConstantRule().metBy(root)

    def testConstantWSpaces(self):
        root = ElementTree.fromstring('<const> hello </const>')
        txt = xml_rules.ConstantRule().getGenerator(root).generateText()
        self.assertEqual('hello', txt)

    def testConstantWLineBreaks(self):
        xml = """<const>
            hello
        </const>"""
        root = ElementTree.fromstring(xml)
        txt = xml_rules.ConstantRule().getGenerator(root).generateText()
        self.assertEqual('hello', txt)

    def testConstantNoText(self):
        xml = """<const></const>"""
        root = ElementTree.fromstring(xml)
        with self.assertRaises(MasherXmlRuleError):
            txt = xml_rules.ConstantRule().getGenerator(root).generateText()


class TestRandomChanceRule(unittest.TestCase):

    def testMetBy(self):
        xml = '<random></random>'
        root = ElementTree.fromstring(xml)
        xml_rules.ConstantRule().metBy(root)

    def testRandomDefaultChance(self):
        xml = """<random><const>hello</const><const>goodbye</const></random>"""
        root = ElementTree.fromstring(xml)
        gen = xml_rules.RandomRule(MockParser()).getGenerator(root)
        self.assertEqual(.5, gen.chance)

    def testRandomChanceGiven(self):
        xml = """
        <random chance='.3'>
            <const>hello</const>
            <const>goodbye</const>
        </random>"""
        # xml = make_xml(xml)
        root = ElementTree.fromstring(xml)
        gen = xml_rules.RandomRule(MockParser()).getGenerator(root)
        self.assertEqual(.3, gen.chance)

    def testRandomDffaultEnding(self):
        xml = """<random><const>hello</const><const>goodbye</const></random>"""
        root = ElementTree.fromstring(xml)
        gen = xml_rules.RandomRule(MockParser()).getGenerator(root)
        self.assertEqual(' ', gen.ending)

    def testRandomEndingGiven(self):
        xml = """<random ending="-"><const>hello</const><const>goodbye</const></random>"""
        root = ElementTree.fromstring(xml)
        gen = xml_rules.RandomRule(MockParser()).getGenerator(root)
        self.assertEqual('-', gen.ending)

    def testRandomToFewConstants(self):
        xml = """<random ending="-"><const>goodbye</const></random>"""
        root = ElementTree.fromstring(xml)
        with self.assertRaises(MasherXmlRuleError):
            gen = xml_rules.RandomRule(MockParser()).getGenerator(root)

    def testRandomToManyConstants(self):
        xml = """<random ending="-"><const>goodbye</const><const>goodbye</const><const>goodbye</const></random>"""
        root = ElementTree.fromstring(xml)
        with self.assertRaises(MasherXmlRuleError):
            gen = xml_rules.RandomRule(MockParser()).getGenerator(root)


class TestFileListRule(unittest.TestCase):

    def testMetBy(self):
        xml = '<filelist></filelist>'
        root = ElementTree.fromstring(xml)
        xml_rules.ConstantRule().metBy(root)

    def testFilelistDefault(self):
        xml = """<filelist ending="-">./test_files/test_names1.txt; ./test_files/test_names2.txt</filelist>"""
        root = ElementTree.fromstring(xml)
        gen = xml_rules.FileListRule().getGenerator(root)

        expected = ["name1", "name2", "name3", "name4", "name5", "name6"]
        self.assertEqual(len(expected), len(gen.words))
        for name in expected:
            assert name in gen.words

    def testFilelistEnding(self):
        xml = """<filelist ending="-">./test_files/test_names1.txt;</filelist>"""
        root = ElementTree.fromstring(xml)
        gen = xml_rules.FileListRule().getGenerator(root)
        self.assertEqual('-', gen.ending)

    def testFilelistNoFiles(self):
        xml = """<filelist></filelist>"""
        root = ElementTree.fromstring(xml)
        with self.assertRaises(MasherXmlRuleError):
            gen = xml_rules.FileListRule().getGenerator(root)


class TestListRule(unittest.TestCase):

    def testMetBy(self):
        xml = '<list></list>'
        root = ElementTree.fromstring(xml)
        xml_rules.ConstantRule().metBy(root)

    def testListDefault(self):
        xml = """<list>word1;word2;word3</list>"""
        expected = ['word1', 'word2', 'word3']
        root = ElementTree.fromstring(xml)
        gen = xml_rules.ListRule().getGenerator(root)
        self.assertEqual(expected, gen.words)

    def testListEnding(self):
        xml = """<list ending='.4'>word1;word2;word3</list>"""
        expected = ['word1', 'word2', 'word3']
        root = ElementTree.fromstring(xml)
        gen = xml_rules.ListRule().getGenerator(root)
        self.assertEqual('.4', gen.ending)

    def testListDetectsListTag(self):
        xml = """<list ending='.4'>word1;word2;word3</list>"""
        expected = ['word1', 'word2', 'word3']
        root = ElementTree.fromstring(xml)
        assert xml_rules.ListRule().metBy(root)

    def testListNoWords(self):
        xml = """<list></list>"""
        root = ElementTree.fromstring(xml)
        with self.assertRaises(MasherXmlRuleError):
            gen = xml_rules.FileListRule().getGenerator(root)


class TestPhraseParser(unittest.TestCase):

    def setUp(self):
        self.rule = xml_rules.PhraseRule(MockParser())

    def testMetBy(self):
        xml = '<phrase></phrase>'
        root = ElementTree.fromstring(xml)
        xml_rules.ConstantRule().metBy(root)

    def testPhraseDefaultCorrectNumberGenerators(self):
        xml = """<phrase> <const>1</const> <const>2</const> </phrase>"""
        root = ElementTree.fromstring(xml)
        gen = self.rule.getGenerator(root)
        self.assertEquals(2, len(gen.generators))

    def testPhraseDefaultEnding(self):
        xml = """<phrase> <const>1</const> <const>2</const> </phrase>"""
        root = ElementTree.fromstring(xml)
        gen = self.rule.getGenerator(root)
        self.assertEquals('', gen.ending)

    def testPhraseDefaultSeparator(self):
        xml = """<phrase> <const>1</const> <const>2</const> </phrase>"""
        root = ElementTree.fromstring(xml)
        gen = self.rule.getGenerator(root)
        self.assertEquals(' ', gen.separator)

    def testPhraseSetEnding(self):
        xml = """<phrase ending="-"> <const>1</const> <const>2</const> </phrase>"""
        root = ElementTree.fromstring(xml)
        gen = self.rule.getGenerator(root)
        self.assertEquals('-', gen.ending)

    def testPhraseSetSeparator(self):
        xml = """<phrase separator="=="> <const>1</const> <const>2</const> </phrase>"""
        root = ElementTree.fromstring(xml)
        gen = self.rule.getGenerator(root)
        self.assertEquals('==', gen.separator)


class MockParser:

    def __init__(self):
        self.index = 0
        self.ls = [1,2,3,4,5,6,7,8,9,10]

    def parse_schema(self, schema):
        gen = ConstantGenerator(str(self.ls[self.index]))
        return gen

if __name__ == "__main__":
    unittest.main()