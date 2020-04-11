import unittest
#Run with: python -m unittest

class MyFirstTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    def test_someThing(self):
        self.assertTrue(True)
        pass