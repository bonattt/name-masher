from random import randint
from random import random

from masher.exceptions import WordMasherParseException
from masher.exceptions import WordMasherUnimplimentedException
from masher.exceptions import WordMasherException

global count
count = 0


class ListGenerator():
    
    def __init__(self, words=[]):
        global count
        self.words = words
        self.count = count
        count+= 1
            
    def isExtensible(self):
        return False
                    
    def generateWordList(self, filepath):
        file = open(filepath, 'r')
        self.words = file.read().split('\n')
        file.close()
        
    def generateText(self):
        index = randint(0,len(self.words)-1)
        return '<' + self.words[index] + ' (' + str(self.count) +') >'
                
class CompositeGenerator():

    def __init__(self, generators=[]):
        self.generators = generators
        
    def isExtensible(self):
        return True
        
    def addGenerator(self, generator):
        self.generator.append(generator)
    
    def generateText(self):
        rn = randint(0, len(self.generators)-1)
        return self.generators[rn].generateText()        
    
    
class ConstantGenerator(): 
    
    def __init__(self, constant):
        self.word = constant
        
    def isExtensible(self):
        return False
        
    def addGenerator(self, generator):
        raise WordMasherUnimplimentedException('method "ConstantGenerator.addGenerator" unimplemented')
    
    def generateText(self):
        return self.word
        
        
class RandomChanceGenerator():
    
    def __init__(self, generator, alt, chance):
        if (chance >= 1) or (chance <= 0):
            raise WordMasherException("RandomChanceGenerator's chance must be within the bounds 1 > [chance] > 0")
        self.generator = generator
        self.alt = alt
        self.chance = chance
        
    def addGenerator(self, generator):
        raise WordMasherUnimplimentedException('method "RandomChanceGenerator.addGenerator" unimplemented')
        
    def isExtensible(self):
        return False
        
    def generateText(self):
        rn = random()
        if rn <= self.chance:
            return self.generator.generateText()
        else:
            return self.alt.generateText()
        
    
class PhraseGenerator():
    
    def __init__(self, generators=[]):
        self.generators = generators
        
    def addGenerator(self, generator):
        self.generators.append(generator)
        
    def isExtensible(self):
        return True
        
    def generateText(self):
        msg = ''
        length = len(self.generators)
        for k in range(length):
            msg += self.generators[k].generateText();
            msg += ' '         
            
        return msg
