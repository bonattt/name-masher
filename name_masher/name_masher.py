# from masher.parsing import DefaultParser
# from temp_module import DefaultParser

from name_masher.masher.parsing import DefaultParser
from name_masher.masher.configuration import Configuration


def run():
    # file = open(schemapath, 'r')
    # schema = file.read()
    # parser = DefaultParser()
    # generator = parser.parse_schema(schema)

    config = Configuration(DefaultParser())
    config.load_from_file('config.json')

    generator = config.get_generator("default")
    all_generators = {"default": generator}

#    wordGen1 = WordGenerator('./masher_files/adj-total.txt');
#    wordGen2 = WordGenerator('./masher_files/verb-destruction.txt');
#    phraseGen = PhraseGenerator([wordGen1, wordGen2])
    while True:
        user_in = input('enter command ~~>').strip()
        if user_in == '':
            print(generator.generateText())

        elif user_in.startswith('q'):
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

        elif user_in in all_generators:
            generator = all_generators[user_in]
            print(generator.generateText())

        else:
            generator = config.get_generator(user_in)
            print("set the active generator to", user_in)
            #     all_generators[user_in] = None
            # else:
            #     print('"'+user_in+'"', "is not a schema.")

    print('exiting shell. Have a nice day! :)')

def read_new_schema(filepath):
    file = open(filepath, 'r')
    schema = file.read()
    parser = DefaultParser()
    generator = parser.parse_schema(schema)
    return generator


def main():
    print('welcome to name masher!');
    run();



if __name__ == "__main__":
    main()