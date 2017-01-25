from random import randint


class DefaultParser():

    def parse_schema(self, schema):
        syllables = schema.split()
        generators = []
        for syl in syllables:
            generators.append(self.parse_syllable(syl))
        return PhraseGenerator(generators)
        
    def parse_syllable(self, syllable):
        try:
            if syllable.startswith('<') and syllable.endswith('>'):
                inner_syllable = syllable[1:-1]
                file = open('./masher_files/' + inner_syllable, 'r')
                filetext = file.read()
                file.close()
                wordGen = WordGenerator()
                wordGen.words = filetext.split('\n')
                return wordGen
                
            elif syllable.startswith('+'):
                wordGen = WordGenerator()
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

        
###############################

class WordGenerator():
    
    def __init__(self, filepath=None):
        if filepath != None:
            self.generateWordList(filepath)
        else:
            self.words = []
            
    def isExtensible(self):
        return False
                    
    def generateWordList(self, filepath):
        file = open(filepath, 'r')
        self.words = file.read().split('\n')
        file.close()
        
    def generateText(self):
        index = randint(0,len(self.words)-1)
        return self.words[index]
                
    
class ConstantGenerator(): 
    
    def __init__(self, constant):
        self.word = constant
        
    def isExtensible(self):
        return False
        
    def addGenerator(self, generator):
        raise WordMasherUnimplimentedException('method "ConstantGenerator.addGenerator" unimplemented')
    
    def generateText(self):
        return self.word
    
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

#################################


class WordMasherException(Exception):
    pass
    
class WordMasherUnimplimentedException(WordMasherException):
    pass
    
class WordMasherParseException(WordMasherException):
    pass
    