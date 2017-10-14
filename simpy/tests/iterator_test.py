import unittest
import os
import simpy
from simpy.tests import get_current_folder_path

class MyTestCase(unittest.TestCase):
    def test_iter_loop(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'simulation_cfg.xml')
        tr = simpy.read_from_xml(xml_path)
        c = 0
        for t in tr:
            c += 1
            self.assertTrue(t.get_name() == 'blabla23')
            self.assertTrue(t.get_param('loss_q') == 1.812)
        self.assertTrue(c == 1)
        self.assertTrue(tr.get_global_param('cross_validation_k') == 40)


if __name__ == '__main__':
    unittest.main()
