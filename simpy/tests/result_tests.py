'''
Created on Oct 14, 2017

@author: haih
'''
import unittest
import simpy
import os
from .tutils import get_current_folder_path

class Test(unittest.TestCase):


    def test_legend(self):
        xml_path = os.path.join(get_current_folder_path(),'resources', 'test_example_overwrite.xml')
        tr = simpy.read_from_xml(xml_path)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_legend']
    unittest.main()