import unittest


class ATest(unittest.TestCase):

    def setUp(self):
        print("setup")
        pass

    def test_a(self):
        self.assertTrue(True)

    def tearDown(self):
        print("tear down")


if __name__ == "__main__":
    print("masher_test.py")
    unittest.main()