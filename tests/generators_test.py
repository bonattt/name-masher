import unittest

from masher.generators import ListGenerator
from masher.generators import ConstantGenerator
from masher.generators import RandomChanceGenerator
from masher.generators import PhraseGenerator

import random


class GenTest(unittest.TestCase):

    def setUp(self):
        random.seed(1)

    def tearDown(self):
        pass

    def test_list_gen(self):
        # randint(1,3) ==> {1, 3, 1, 2 ...}
        ls = ["word1", "word2", "word3"]
        gen = ListGenerator(ls, ending='')
        self.assertEquals("word1", gen.generateText())
        self.assertEquals("word3", gen.generateText())
        self.assertEquals("word1", gen.generateText())
        self.assertEquals("word2", gen.generateText())

    def test_list_gen_ending(self):
        # randint(1,3) ==> {1, 3, 1, 2 ...}
        ls = ["word1", "word2", "word3"]
        gen = ListGenerator(ls, ending=' ')
        self.assertEquals("word1 ", gen.generateText())
        self.assertEquals("word3 ", gen.generateText())
        self.assertEquals("word1 ", gen.generateText())
        self.assertEquals("word2 ", gen.generateText())

    def test_constant(self):
        word = "awpodj"
        gen = ConstantGenerator(word)
        for k in range(100):
            self.assertEqual(word, gen.generateText())

    def test_rand(self):
        # random() ==> {.134, .847, .764, .255, ...}
        word1 = "first gen"
        out1 = ConstantGenerator(word1)
        word2 = "alt gen"
        out2 = ConstantGenerator(word2)
        gen = RandomChanceGenerator(out1, out2, .5, ending='')
        self.assertEqual(word1, gen.generateText())
        self.assertEqual(word2, gen.generateText())

    def test_rand_ending(self):
        # random() ==> {.134, .847, .764, .255, ...}
        word1 = "first gen"
        out1 = ConstantGenerator(word1)
        word2 = "alt gen"
        out2 = ConstantGenerator(word2)
        gen = RandomChanceGenerator(out1, out2, .5, ending=' ')
        self.assertEqual(word1+' ', gen.generateText())
        self.assertEqual(word2+' ', gen.generateText())

    def test_phrase(self):
        gen = PhraseGenerator([ConstantGenerator("word 1"), ConstantGenerator("word 2")], separator='', ending='')
        self.assertEqual("word 1word 2", gen.generateText())

    def test_phrase_separetor(self):
        gen = PhraseGenerator([ConstantGenerator("word 1"), ConstantGenerator("word 2")], separator=' ', ending='')
        self.assertEqual("word 1 word 2 ", gen.generateText())

    def test_phrase_ending(self):
        gen = PhraseGenerator([ConstantGenerator("word 1"), ConstantGenerator("word 2")], separator='', ending=' ')
        self.assertEqual("word 1word 2 ", gen.generateText())


if __name__ == "__main__":
    print("generatiors_test.py")
    unittest.main()