
from masher.generators import CompositeGenerator
from masher.generators import ListGenerator
from masher.generators import ConstantGenerator
from masher.generators import PhraseGenerator
from masher.generators import RandomChanceGenerator

from masher.exceptions import WordMasherParseException


class ConstantRule:

    def metBy(self, syllable):
        if (syllable.startswith('"') and syllable.endswith('"')) or (syllable.startswith("'") and syllable.endswith("'")):
            return True
        
        return False
        
    def getGenerator(self, syllable):
        return ConstantGenerator(syllable[1:-1])
        
# rule: ?(_chance, _generator_, _elseGenereator_)
# else generator is optional, it defaults to the constant ''
class RandomRule:

    def __init__(self, parser):
        self.parser = parser

    def metBy(self, syllable):
        if (syllable.startswith('?(') and syllable.endswith(')')):
            return True
        return False
        
    def getGenerator(self, syllable):
        subsyllable = syllable[2:-1]
        subsyllable = subsyllable.split(',')
        chance = float(subsyllable[0])
        generator = self.parser.parse_schema(subsyllable[1])
        if len(subsyllable) == 3:
            elseGen = self.parser.parse_schema(subsyllable[2])
        elif len(subsyllable) == 2:
            elseGen = ConstantGenerator('')
        else:
            raise WordMasherParseException('RandomRule vilation: incorrect number of arguments.' + str(len(subsyllable)))
        
        return RandomChanceGenerator(generator, elseGen, chance)
        

class ListRule:

    def metBy(self, syllable):
        if syllable.startswith('<') and syllable.endswith('>'):
            return True
        return False
        
    def getGenerator(self, syllable):
        inner_syllable = syllable[1:-1].split(' && ')
        wordGen = ListGenerator([])
        for filename in inner_syllable:
            file = open('./name_files/' + filename.strip(), 'r')
            filetext = file.read()
            file.close()
            wordGen.words += filetext.split('\n')
        return wordGen
        
        
class EnchantmentBonusRule:
    
    def metBy(self, syllable):
        if syllable.startswith('+'):
            return True
        return False
        
    def getGenerator(self, syllable):
        wordGen = ListGenerator()
        inner_syllables = (syllable[1:].split(':'))
        start = int(inner_syllables[0])
        end = int(inner_syllables[1])
        wordGen.words = range(start, end)
        return wordGen
      
      
class PhraseRule:

    def __init__(self, parser):
        self.parser = parser
    
    def metBy(self, syllable):
        if syllable.startswith('{') and syllable.endswith('}'):
            return True
        return False
    
    def getGenerator(self, syllable):
        syllables = syllable[1:-1].split(' | ')
        generators = []
        for seg in syllables:
            generators.append(self.parser.parse_schema(seg))
            
        return PhraseGenerator(generators)
