import random

from masher.exceptions import WordMasherParseException
from masher.exceptions import WordMasherUnimplimentedException
from masher.exceptions import WordMasherException


class ListGenerator:
    """this generator picks a random word from a stored list of words."""

    def __init__(self, words, ending=' '):
        # cannot use words=[] because of a very strange bug I got where python
        # used the SAME empty list as the default value for each ListGenerator.
        # The result was that every ListGenerator instance shared the same
        # self.words value.
        self.words = words
        self.ending = ending

    def __str__(self):
        return "<List Generator (" + str(len(self.words)) + " words)>"

    def __repr__(self):
        return str(self)

    def isExtensible(self):
        return False

    def generateWordList(self, filepath):
        file = open(filepath, 'r')
        self.words = file.read().split('\n')
        file.close()

    def generateText(self):
        index = random.randint(0,len(self.words)-1)
        return self.words[index] + self.ending


class CompositeGenerator:
    """the composite generator stores multiple generators, and generates
    a word for only one of these generators (selected randomly)"""

    def __init__(self, generators, ending=' '):
        self.generators = generators
        self.ending = ending

    def __str__(self):
        return "<Composite Generator " + str(self.generators) + " >" +\
               self.ending

    def __repr__(self):
        return str(self)

    def isExtensible(self):
        return True

    def addGenerator(self, generator):
        self.generator.append(generator)

    def generateText(self):
        rn = random.randint(0, len(self.generators)-1)
        return self.generators[rn].generateText()


class ConstantGenerator:
    """the constant generator is given a constant at creation, and always returns this value"""

    def __init__(self, constant):
        self.word = constant

    def __str__(self):
        return "<Constant Generator '" + self.word + "'>"

    def __repr__(self):
        return str(self)

    def isExtensible(self):
        return False

    def addGenerator(self, generator):
        raise WordMasherUnimplimentedException('method "ConstantGenerator.'
                                               'addGenerator" unimplemented')

    def generateText(self):
        return self.word


class RandomChanceGenerator:
    """the random chance generator has a weighted change to
     generate a word from one of two stored generators"""

    def __init__(self, generator, alt, chance, ending=" "):
        if (chance >= 1) or (chance <= 0):
            raise WordMasherException("RandomChanceGenerator's chance must "
                                      "be within the bounds 1 > [chance] > 0")
        self.generator = generator
        self.alt = alt
        self.chance = chance
        self.ending = ending

    def __str__(self):
        return "<Random Chance Generator (" +\
               str(self.chance) + ', ' + str(self.generator) +\
               ', ' + str(self.alt) + ")>" +\
                self.ending

    def __repr__(self):
        return str(self)

    def addGenerator(self, generator):
        raise WordMasherUnimplimentedException('method "RandomChanceGenerator.'
                                               'addGenerator" unimplemented')

    def isExtensible(self):
        return False

    def generateText(self):
        rn = random.random()
        if rn <= self.chance:
            return self.generator.generateText() + self.ending
        else:
            return self.alt.generateText() + self.ending


class PhraseGenerator:
    """the PhraseGenerator stores multiple generators, and it
    generates a word from each generator in the order they are stored"""

    def __init__(self, generators, separator='', ending=''):
        self.generators = generators
        self.separator = separator
        self.ending = ending

    def __str__(self):
        return "<Phrase Generator " + str(self.generators) + ">"

    def __repr__(self):
        return str(self)

    def addGenerator(self, generator):
        self.generators.append(generator)

    def isExtensible(self):
        return True

    def generateText(self):
        msg = ''
        length = len(self.generators)
        for k in range(length):
            msg += self.generators[k].generateText() + self.separator

        return msg + self.ending
