import unittest
import numpy as np
import simpy


class MyTestCase(unittest.TestCase):
    def test_something(self):
        n_epoch = 10
        n_batch = 100
        ra = simpy.ResultAppender(['d', 'l'], {'d': simpy.data_concat, 'l': simpy.data_concat})
        for _ in range(n_epoch):
            for _ in range(n_batch):
                d = np.random.randn(16, 100)
                l = np.random.rand(1)
                ra.update_result({'d': d, 'l': l})
            ra.update_record()


if __name__ == '__main__':
    unittest.main()
