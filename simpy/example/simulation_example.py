'''
Created on Nov 6, 2017

@author: haih
'''
import simpy
from simpy.tests.tutils import get_current_folder_path
import os
import numpy as np


class ExampleSimulation(simpy.SimulationManger):
    def __init__(self, xml_path):
        self.sc = self.create(xml_path)  # generate simulation control

    def run(self):
        for t in self.sc.get_tests():  # loop over test
            result = t.generate_test_result('res_a', np.random.rand(1))
            self.sc.add_result(result)

        for i in self.sc.get_results():
            print(i.get_test_name())
            print(i.get_result('res_a'))


if __name__ == "__main__":
    xml_path = os.path.join(get_current_folder_path(), 'simulation_cfg.xml')  # set xml path
    test = ExampleSimulation(xml_path)  # init simulation
    test.run()  # run simulation
