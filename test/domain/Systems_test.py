import unittest
from database import getDbConnection
from domain.Systems import System, Systems
from systems.systemIO import systemTypes


class MyTestCase(unittest.TestCase):
    def test_normal_ma(self):
        systems = Systems(getDbConnection("sp"))
        systems.addSystem(System([10, 20, 30], systemTypes.NORMAL))
        systems.systems[0].stats.print()

    def test_versus(self):
        systems = Systems(getDbConnection("sp"))
        systems.addSystem(System([[10,20,30],[40,50,60]], systemTypes.VERSUS))
        systems.systems[0].stats.print()


if __name__ == '__main__':
    unittest.main()
