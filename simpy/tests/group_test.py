import unittest
from simpy.tests.tutils import get_current_folder_path
import os
import simpy


class MyTestCase(unittest.TestCase):
    def test_group_read(self):
        xml_path = os.path.join(get_current_folder_path(), 'resources', 'simulation_cfg_groups.xml')
        tr = simpy.read_from_xml(xml_path)
        self.assertTrue(tr.test_list.__len__() == 4)

    def test_group_read_not(self):
        xml_path = os.path.join(get_current_folder_path(), 'resources', 'simulation_cfg_groups_not.xml')
        tr = simpy.read_from_xml(xml_path)
        self.assertTrue(tr.test_list.__len__() == 2)


if __name__ == '__main__':
    unittest.main()
