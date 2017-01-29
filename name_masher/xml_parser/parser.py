from xml.etree import ElementTree


class MasherXmlParser:

    DEFAULT_END_CHAR = " "
    DEFAULT_SEPARATOR = ""

    def __init__(self, rules=[]):
        self.rules = []
        for rule in rules:
            self.add_rule(rule)
        self.end_char = MasherXmlParser.DEFAULT_END_CHAR
        self.separator = MasherXmlParser.DEFAULT_SEPARATOR

    def default_setup(self):
        pass

    def enable_debug_printing(self):
        self.add_rule(PrintRule())

    def add_rule(self, rule):
        self.rules.append(rule)

    def parse_schema(self, schema):
        element = ElementTree.fromstring(schema)
        return self.begin_parse(element)

    def parse_file(self, file_path):
        etree = ElementTree.parse(file_path)
        element = etree.getroot()
        return self.begin_parse(element)

    def begin_parse(self, element):
        if "endChar" in element.attrib:
            self.end_char = element.attrib["endChar"]
        else:
            self.end_char = MasherXmlParser.DEFAULT_END_CHAR

        if "separator" in element.attrib:
            self.separator = element.attrib["separator"]
        else:
            self.separator = MasherXmlParser.DEFAULT_SEPARATOR

        return self.parse_tree(element)

    def parse_tree(self, element, layer=0):
        generators = []
        self.apply_rules(element, layer)
        for child in element:
            generators += self.parse_tree(child, layer+1)
        return generators

    def apply_rules(self, element, layer):
        generators = []
        for rule in self.rules:
            generators += rule.apply_rule(element, layer)
        return generators


class PrintRule():

    def apply_rule(self, element, layer):
        msg = '\t' * layer
        msg += str(element.tag) + str(element.attrib)
        if element.text:
            msg += element.text
        print(msg.replace('\n', ''))
        return []