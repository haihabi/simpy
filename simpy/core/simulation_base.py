'''
Created on Nov 6, 2017

@author: haih
'''
import simpy


class SimulationManger():
    @classmethod
    def create(cls, xml_path):
        tr = simpy.read_from_xml(xml_path)
        return SimulationManger.Simulation(tr)

    def run(self):
        raise NotImplemented

    class Simulation():
        def __init__(self, tr):
            self.tr = tr
            self.rc = self.tr.generate_result_container()

        def get_tests(self):
            return self.tr.generate_test_iterator()

        def add_result(self, result):
            self.rc.add_result(result)

        def reset(self):
            return SimulationManger.Simulation(self.tr)

        def get_results(self):
            return self.rc.recreate_iterator()
