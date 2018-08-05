import simpy


class CrossValidationV2(object):
    def __init__(self, data_set: simpy.data_sets.DataWrapper, result_merge_function, k_size=5):
        self.data_set = data_set.shuffle()
        self._i = 0
        self.k_size = k_size
        self._split_factor = 1 / k_size
        self.rmf = result_merge_function
        self.crd = {k: [] for k in result_merge_function.keys()}  # current result dict

    def __iter__(self):
        # Return the iterable object (self)
        return self

    def __next__(self):
        if self._i < self.k_size:
            print("Starting Fold:" + str(self._i + 1))
            data_out = self.data_set.split([1 - self._split_factor, self._split_factor])
            self.data_set.cycle_shift(int(self.data_set.get_number_of_samples() * self._split_factor))
            self._i += 1
            return data_out
        else:
            raise StopIteration

    def update_result(self, ra):
        assert isinstance(ra, simpy.ResultAppender)
        [l.append(ra.get_record(k)) for k, l in self.crd.items()]

    def merge_result(self):
        return {k: self.rmf.get(k)(l) for k, l in self.crd.items()}

    def plot_result(self, plot_cfg):
        assert isinstance(plot_cfg, simpy.PlotConfiguration)
        plot_cfg.plot_result(self.merge_result())

    def get_result_key_value_per(self):
        result = []
        [result.extend([k, v]) for k, v in self.merge_result().items()]
        return result
