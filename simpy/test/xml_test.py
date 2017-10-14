import unittest
from .tutils import get_current_folder_path
import os
from simpy.core.xml.xml_read import read_xml

class MyTestCase(unittest.TestCase):
    def test_sub_tree(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'xmltest.xml')
        xt = read_xml(xml_path)
        res = xt.get_sub_trees('global_params')
        self.assertTrue(isinstance(res, list))
        self.assertTrue(res.__len__() > 0)
        res = xt.get_sub_trees('global_par222ams')
        self.assertTrue(res.__len__() == 0)

    def test_tree_attr(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'xmltest.xml')
        xt = read_xml(xml_path)
        res = xt.get_sub_trees('global_params')
        res[0].get_tree_attr()
        self.assertTrue(res[0].get_tree_attr().get('fun') == '1')


if __name__ == '__main__':
    unittest.main()
