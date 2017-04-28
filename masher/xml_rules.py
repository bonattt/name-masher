
from masher.generators import CompositeGenerator
from masher.generators import ListGenerator
from masher.generators import ConstantGenerator
from masher.generators import PhraseGenerator
from masher.generators import RandomChanceGenerator

from masher.exceptions import WordMasherParseException

def add_default_rules(parser):
    parser.add_rule(ConstantRule())
    parser.add_rule(ListRule())
    parser.add_rule(FileListRule())
    parser.add_rule(RandomRule(parser))
    parser.add_rule(PhraseRule(parser))
    parser.add_rule(NewlineRule())


class MasherXmlRuleError(Exception):
    pass


def clean_text_node(txt):
    if not txt:
        return
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\t', '    ')
    txt = txt.strip()
    return txt

def get_attrib(tree, attr_name, default):
    if attr_name in tree.attrib:
        return tree.attrib[attr_name]
    else:
        return default

def get_ending(tree):
    return get_attrib(tree, 'ending', ' ')


class NewlineRule:

    def metByTag(self, tag):
        if tag == 'br':
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        return ConstantGenerator('\n')


class ConstantRule:

    def metByTag(self, tag):
        if tag == 'const':
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        txt = clean_text_node(tree.text)

        if 'start' in tree.attrib:
            txt = tree.attrib['start'] + txt
        elif 'end' in tree.attrib:
            txt = txt + tree.attrib['end']

        if not txt or txt == '':
            raise MasherXmlRuleError("const tag contains bad text")
        return ConstantGenerator(txt)


# rule: ?(_chance, _generator_, _elseGenereator_)
# else generator is optional, it defaults to the constant ''
class RandomRule:

    def __init__(self, parser, chance=".5", ending=" "):
        self.parser = parser
        self.default_chance = chance
        self.default_ending = ending

    def metByTag(self, tag):
        if tag == 'random':
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        if len(tree) > 2:
            raise MasherXmlRuleError("random tag has too many child nodes(" + str(len(tree)) + ")")
        if len(tree) < 2:
            raise MasherXmlRuleError("random tag has too few child nodes(" + str(len(tree)) + ")")

        chance = float(get_attrib(tree, 'chance', self.default_chance))
        ending = get_attrib(tree, 'ending', self.default_ending)

        gen1 = self.parser.parse_tree(tree[0])
        gen2 = self.parser.parse_tree(tree[1])
        return RandomChanceGenerator(gen1, gen2, chance, ending)


class FileListRule:

    def __init__(self, ending=' '):
        self.default_ending = ending

    def metByTag(self, tag):
        if tag == 'listfile':
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        file_names = []
        if not tree.text:
            raise MasherXmlRuleError("filelist tag with no text")

        for name in tree.text.split(';'):
            name = name.strip()
            if name != '':
                file_names.append(name)

        if len(file_names) == 0:
            raise MasherXmlRuleError('listfile tag with no file paths given')

        ending = get_attrib(tree, 'ending', self.default_ending)

        words = []
        for name in file_names:
            f = open(name)
            new_words = f.read().split('\n')
            f.close()
            words += new_words

        return ListGenerator(words, ending)


class ListRule:

    def __init__(self, ending=' '):
        self.default_ending = ending

    def metByTag(self, tag):
        if tag == 'list':
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        ending = get_attrib(tree, 'ending', self.default_ending)
        text = clean_text_node(tree.text)
        words = text.split(';')
        clean_words = []
        for i in range(len(words)):
            new_word = words[i].strip()
            if not new_word: continue
            if new_word == '': continue
            clean_words.append(new_word)

        return ListGenerator(clean_words, ending)


class PhraseRule:

    def __init__(self, parser, ending='', separator=''):
        self.parser = parser
        self.default_ending = ending
        self.default_separator = separator

    def metByTag(self, tag):
        if tag == "phrase":
            return True
        return False

    def metBy(self, tree):
        return self.metByTag(tree.tag)

    def getGenerator(self, tree):
        generators = []
        for child in tree:
            try:
                new_gen = self.parser.parse_tree(child)
                generators.append(new_gen)
            except MasherXmlRuleError as e:
                print("warning: phrase sub-generator failed to build")

        separator = get_attrib(tree, "separator", self.default_separator)
        ending = get_attrib(tree, "ending", self.default_ending)

        if len(generators) == 0:
            raise MasherXmlRuleError("phrase tag with no generators ")

        return PhraseGenerator(generators, separator, ending)
