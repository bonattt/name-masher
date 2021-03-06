# from masher.parsing import DefaultParser
# from temp_module import DefaultParser

from masher.xml_parsing import XParser
from masher.xml_rules import add_default_rules
from masher.parsing import DefaultParser
from masher.configuration import Configuration


def build_parser():
    parser = XParser()
    add_default_rules(parser)
    return parser


def run():
    # file = open(schemapath, 'r')
    # schema = file.read()
    # parser = DefaultParser()
    # generator = parser.parse_schema(schema)
    parser = build_parser()
    config = Configuration(parser)
    # config = Configuration(DefaultParser())
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
            save_words_to_file()

        # elif user_in.startswith('config '):
        #     try:
        #         new_schema = user_in[7:]
        #         generator = parser.parse_schema(schema)
        #     except Exception as e:
        #         print('an error occured parsing new config')

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


def save_words_to_file(user_in, generator):
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