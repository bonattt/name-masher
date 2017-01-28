from random import randint
from random import random

from masher.exceptions import WordMasherParseException
from masher.exceptions import WordMasherUnimplimentedException
from masher.exceptions import WordMasherException


class ListGenerator:

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
        index = randint(0,len(self.words)-1)
        return self.words[index] + self.ending


class CompositeGenerator:

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
        rn = randint(0, len(self.generators)-1)
        return self.generators[rn].generateText()


class ConstantGenerator:

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
        rn = random()
        if rn <= self.chance:
            return self.generator.generateText()
        else:
            return self.alt.generateText()


class PhraseGenerator:

    def __init__(self, generators, separator=''):
        self.generators = generators
        self.separator = separator

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

        return msg
