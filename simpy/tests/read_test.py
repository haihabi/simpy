import unittest
from simpy.tests import get_current_folder_path
import os
import simpy
from enum import Enum


class MyTestCase(unittest.TestCase):
    def test_read(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'simulation_cfg.xml')
        tr = simpy.read_from_xml(xml_path)
        self.assertTrue(tr.test_list.__len__() == 2)
        self.assertTrue(isinstance(tr.test_list, list))
        self.assertTrue(tr.param_configurations.__len__() == 2)
        self.assertTrue(isinstance(tr.param_configurations, dict))
        self.assertTrue(isinstance(tr.global_param, dict))

    def test_enum(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'enum_example.xml')
        tr = simpy.read_from_xml(xml_path)

        class TestEnum(Enum):
            Test0 = 0
            Test2 = 1
            Test1 = 2

        for t in tr:
            er = t.read_enum(TestEnum)
            self.assertTrue(isinstance(er, list))
            self.assertTrue(er.__len__() == 2)
            self.assertTrue(TestEnum.Test0 in er)
            self.assertTrue(TestEnum.Test2 in er)

    def test_overwrite(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'test_example_overwrite.xml')
        tr = simpy.read_from_xml(xml_path)
        for t in tr:
            self.assertTrue(t.get_param('decay_steps') == 20)


if __name__ == '__main__':
    unittest.main()
