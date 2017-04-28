import name_masher_shell

from masher.parsing import DefaultParser
from masher.configuration import Configuration


CONFIG = Configuration()

def get_generator(generator_name="default"):
    config = Configuration(DefaultParser())
    config.load_from_file('config.json')
    generator = config.get_generator(generator_name)
    return generator


def load_generator(generator_name="default"):
    config = Configuration(DefaultParser())
    config.load_from_file('config.json')
    generator = config.get_generator(generator_name)
    return generator


def get_name():
