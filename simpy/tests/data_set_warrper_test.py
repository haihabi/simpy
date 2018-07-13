import unittest
import simpy
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_split(self):
        train = simpy.data_sets.Data(np.random.randn(10, 2))
        validation = simpy.data_sets.Data(np.random.randn(10, 2))
        dsw = simpy.data_sets.DataWrapper([train, validation], 2)
        dsw0, dsw1 = dsw.split([0.5, 0.5])
        self.assertTrue((dsw0.n + dsw1.n) == 10)
        dsw0, dsw1 = dsw.split([0.7, 0.3])
        self.assertTrue((dsw0.n + dsw1.n) == 10)


if __name__ == '__main__':
    unittest.main()
