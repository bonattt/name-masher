import name_masher_shell

from masher.xml_parsing import XParser
from masher.xml_rules import add_default_rules
from masher.configuration import Configuration


def build_parser():
    parser = XParser()
    add_default_rules(parser)
    return parser


def get_generator(generator_name="default"):
    config = Configuration(build_parser())
    config.load_from_file('config.json')
    generator = config.get_generator(generator_name)
    return generator


def load_generator(generator_name="default"):
    config = Configuration(XParser())
    config.load_from_file('config.json')
    generator = config.get_generator(generator_name)
    return generator


def get_name():
    pass