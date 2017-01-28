
from name_masher.masher.generators import PhraseGenerator
# from masher.generators import ListGenerator
# from masher.generators import ConstnantGenerator

from name_masher.masher.exceptions import WordMasherParseException
from name_masher.masher.exceptions import WordMasherException

from name_masher.masher.parsing_rules import ConstantRule
from name_masher.masher.parsing_rules import ListRule
from name_masher.masher.parsing_rules import EnchantmentBonusRule
from name_masher.masher.parsing_rules import PhraseRule
from name_masher.masher.parsing_rules import RandomRule


class DefaultParser:

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
            raise e # WordMasherException('unrecognized error: ' + str(e))
