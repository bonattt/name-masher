import unittest
from name_masher.masher.configuration import Configuration
import os.path

class ConfigTest(unittest.TestCase):

    SCHEMA_NAME = "test configuration"
    FILE_PATH = "./testconfig.json"

    def setUp(self):
        self.config = Configuration(MochParser())
        print("Abspath:", os.path.abspath(ConfigTest.FILE_PATH))
        self.config.load_from_file(ConfigTest.FILE_PATH)

    def tearDown(self):
        del self.config

    def test_load_from_file(self):
        self.assertEquals("test config value", self.config.get("test config key"))

    def test_get_schema(self):
        schema = self.config.get_schema(ConfigTest.SCHEMA_NAME)
        self.assertEqual("test schema config text", schema)

    def test_get_generator(self):
        generator = self.config.get_generator(ConfigTest.SCHEMA_NAME)
        self.assertEqual("generator", generator)

class MochParser():

    def parse_schema(self, schema):
        return "generator"

if __name__ == "__main__":
    print("configuration_test.py")
    unittest.main()