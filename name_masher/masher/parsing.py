
from masher.generators import PhraseGenerator
# from masher.generators import ListGenerator
# from masher.generators import ConstnantGenerator

from masher.exceptions import WordMasherParseException
from masher.exceptions import WordMasherException

from masher.parsing_rules import ConstantRule
from masher.parsing_rules import ListRule
from masher.parsing_rules import EnchantmentBonusRule
from masher.parsing_rules import PhraseRule
from masher.parsing_rules import RandomRule

class DefaultParser():

    def __init__(self):
        self.rules = []
        self.addRule(ConstantRule())
        self.addRule(ListRule())
        self.addRule(EnchantmentBonusRule())
        self.addRule(PhraseRule(self))
        self.addRule(RandomRule(self))
        
    def addRule(self, rule):
        self.rules.append(rule)

    def parse_schema(self, schema):
        schema = schema.replace('\n', '')
        syllables = schema.split(';')
        generators = []
        for k in range(len(syllables)):
            print("DEBUG - parsing rule:", k, syllables[k])
            generators += self.parse_syllable(syllables[k])
        return PhraseGenerator(generators)
        
    def parse_syllable(self, syllable):
        syllable = syllable.strip()
        try:
            new_generators = []
            rule_met = False
            for k in range(len(self.rules)):
                rule = self.rules[k]
                if rule.metBy(syllable):
                    rule_met = True
                    new_generators.append(rule.getGenerator(syllable))
            if not rule_met:
                raise WordMasherParseException('Unknown parsing syllable "' + syllable + '"')
            return new_generators
        except WordMasherException as e:
            raise e
        except Exception as e:
            raise WordMasherException('unrecognized error: ' + str(e)) 
    
"""    
    def old_parse_syllable(self, syllable):
        try:
            if syllable.startswith('<') and syllable.endswith('>'):
                inner_syllable = syllable[1:-1]
                file = open('./masher_files/' + inner_syllable, 'r')
                filetext = file.read()
                file.close()
                wordGen = ListGenerator()
                wordGen.words = filetext.split('\n')
                return wordGen
                
            elif syllable.startswith('+'):
                wordGen = ListGenerator()
                inner_syllables = (syllable[1:].split(':'))
                start = int(inner_syllables[0])
                end = int(inner_syllables[1])
                wordGen.words = range(start, end)
                return wordGen
                
            elif (syllable.startswith("'") and syllable.endswith("'")) or (syllable.startswith('"') and syllable.endswith('"')):
                inner_syllable = syllable[1:-1]
                wordGen = ConstantGenerator(inner_syllable)
                return wordGen
                
            else:
                raise WordMasherParseException('Unknown parsing syllable "' + syllable + '"')
                
        except WordMasherException as e:
            print('ERROR!')
            print(e.msg)
            return ConstantGenerator('')
        except Exception as e:
            raise e     # todo: something 
"""
        