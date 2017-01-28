import json
import os.path
from masher.exceptions import WordMasherConfigException

class Configuration:

    def __init__(self, parser):
        self.values = {}
        self.schemas = {}
        self.generators = {}
        self.parser = parser

    def load_from_file(self, file_path):
        file = open(file_path, 'r')
        config_file_text = file.read()
        file.close()
        self.values = json.loads(config_file_text)
        schema_path = self.values["default_schema"]
        self.schemas["default"] = self.read_schema_from_file(schema_path)
        self.load_new_generator("default")

    def get(self, key):
        return self.values[key]

    def get_schema(self, name):
        if not name in self.schemas:
            self.load_new_schema(name)
        return self.schemas[name]

    def load_new_schema(self, name):
        if not name in self.values["schemas"]:
            raise WordMasherConfigException("trying to load non existant schema")
        schema_path = self.values["schemas"][name]
        self.schemas[name] = self.read_schema_from_file(schema_path)
        print("loaded new schema", name)

    def read_schema_from_file(self, schema_path):
        if not os.path.isfile(schema_path):
            raise WordMasherConfigException("Schema file '" + schema_path + "' could not be read!")
        file = open(schema_path, 'r')
        new_schema = file.read()
        file.close()
        print("read new schema from file '" + schema_path + "'")
        return new_schema

    def load_new_generator(self, name):
        if not name in self.schemas:
            self.load_new_schema(name)
        self.generators[name] = self.parser.parse_schema(self.schemas[name])
        print("loaded new generator,", name)

    def get_generator(self, name):
        if not name in self.generators:
            self.load_new_generator(name)
        return self.generators[name]


