# from masher.parsing import DefaultParser
# from temp_module import DefaultParser

from masher.parsing import DefaultParser
import json


def run():
    file = open('./config.json', 'r')
    configfiletext = file.read()
    file.close()
    config = json.loads(configfiletext)
    schemapath = config["default_schema"]
    print("schemapath:", schemapath)

    file = open(schemapath, 'r')
    schema = file.read()
    parser = DefaultParser()
    generator = parser.parse_schema(schema)
    
    
#    wordGen1 = WordGenerator('./masher_files/adj-total.txt');
#    wordGen2 = WordGenerator('./masher_files/verb-destruction.txt');
#    phraseGen = PhraseGenerator([wordGen1, wordGen2])
    while True:
        user_in = input('enter command ~~>')
        if user_in.startswith('q'):
            break
            
        elif user_in.startswith('save '):
            commands = user_in.split(' ')
            num = int(commands[1])
            if len(commands) > 2:
                filepath = commands[2]
            else:
                filepath = './output.txt'
                
            file = open(filepath, 'w')
            for k in range(num):
                file.write(generator.generateText())
                file.write('\n\n')
            file.close()
            
        elif user_in.startswith('config '):
            try:
                new_schema = user_in[7:]
                generator = parser.parse_schema(schema)
            except Exception as e:
                print('an error occured parsing new config')
            
        else:
            print(generator.generateText())
            
    print('exiting shell. Have a nice day! :)')


def main():
    print('welcome to name masher!');    
    run();



if __name__ == "__main__":
    main()