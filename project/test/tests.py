import unittest
#Run with: python -m unittest
from ..calculation import calcSysCols

class MyFirstTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    def test_someThing(self):
        self.assertTrue(True)
        pass

    # systems: a 2d array of systems [[2,4,6,8],[10,12,14],[16,18,20],[22,24,26]]
    # data: The data to calculate the sys cols on
    def test_calcSysCols(self):
        systems = [[2]]
        data = [1,2,3,4,5,6,7,8,9,10]
        dbConnection = None
        calculated = calcSysCols(systems, data, dbConnection)
        self.assertEquals(calculated,[]) #TODO