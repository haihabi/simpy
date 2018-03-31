import simpy


class Bootstrapping(object):
    def __init__(self, dsw, probability_function, enable=True):
        assert isinstance(dsw, simpy.data_sets.DataWrapper)
        assert isinstance(enable, bool)
        self.dsw = dsw
        self.enable = enable
        self.er = None
        self.pf = probability_function
        self.first_iteration = True

    def get_training_wrapper(self):
        if self.enable and not self.first_iteration:
            if self.er is None:
                raise Exception('please update loss values')
            pv = self.pf(self.er)
            self.er = None
            return self.dsw.change_shuffle_index(shuffle_index=pv)
        else:
            self.first_iteration = False
            return self.dsw.shuffle()

    def get_base_wrapper(self):
        return self.dsw

    def update_epoch_result(self, epoch_result):
        self.er = epoch_result
