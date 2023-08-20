import unittest
from typing import List

import domain
from datasources import alphaVantage

class TestAlphaVantage(unittest.TestCase):

    def test_get_datapoints(self):
        datapoints: List[domain.Datapoint] = alphaVantage.getDatapoints('IBM', '5min')
        pass
