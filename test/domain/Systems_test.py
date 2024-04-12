import unittest
from database import getDbConnection, load_datapoints
from domain.Systems import System, Systems
from systems.systemIO import systemTypes


class SystemsTestClass(unittest.TestCase):
    def test_normal_ma(self):
        db_connection = getDbConnection("sp")
        datapoints = load_datapoints(db_connection)
        systems = Systems()
        systems.setDatapoints(datapoints)
        systems.addSystem(System([10, 20, 30], systemTypes.NORMAL))
        systems.systems[0].stats.print()

    def test_versus(self):
        db_connection = getDbConnection("sp")
        datapoints = load_datapoints(db_connection)
        systems = Systems()
        systems.setDatapoints(datapoints)
        systems.addSystem(System([[10,20,30],[40,50,60]], systemTypes.VERSUS))
        systems.systems[0].stats.print()

    def test_determineAllEquivalentDivisors(self):
        system = System()
        eq = system.determineAllEquivalentDivisors([20], 4)
        print(eq)


if __name__ == '__main__':
    unittest.main()
