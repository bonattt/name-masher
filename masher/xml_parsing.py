from xml.etree import ElementTree
from masher.xml_rules import MasherXmlRuleError


class MasherXmlParseError(Exception):
    pass


class XParser():

    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        pass

    def parse_file(self, filepath):
        f = open(filepath)
        schema = f.read()
        f.close()
        return self.parse_schema(schema)

    def parse_schema(self, schema):
        root = ElementTree.fromsting(schema)
        return self.parse_tree(root)

    def parse_tree(self, tree):
        for rule in self.rules:
            if rule.metBy(tree):
                return rule.getGenerator(tree)

        raise MasherXmlRuleError('no parser rules applied to tag "' + tree.tag + '"')


