import simpy
import numpy as np


class CrossValidation(object):
    def __init__(self, data, target, result_merge_function, k_size=5):

        self.is_data_list = not isinstance(data, np.ndarray)
        self.is_target_list = not isinstance(target, np.ndarray)
        self._check_input(data, self.is_data_list)
        self._check_input(target, self.is_target_list)

        self.rmf = result_merge_function
        self.data = data
        self.target = target

        self.size = self._cross_check()

        self.k_size = k_size
        self.crd = {k: [] for k in self.rmf.keys()}  # current result dict
        self.fs = self._set_k_size(self.k_size, self.size)  # fold size
        self.fi = 0  # fold index
        self._data_shuffle()

    def _data_shuffle(self):
        index = simpy.data_sets.data_shuffle_index(self.size)
        self.data = self._shuffle_single(self.data, index, self.is_data_list)
        self.target = self._shuffle_single(self.target, index, self.is_target_list)

    @staticmethod
    def _shuffle_single(data, index, is_list):
        data_new = data.copy()
        if is_list:
            for i, d in enumerate(data):
                data_new[i] = d[index, :]
        else:
            data_new = data[index, :]
        return data_new

    @staticmethod
    def _check_input(data_input, is_list):
        if not (isinstance(data_input, list) or isinstance(data_input, np.ndarray)):
            raise Exception('input data must be of type list or numpy ndarray')
        if is_list and np.any(np.asarray([d.shape[0] for d in data_input]) != data_input[0].shape[0]):
            raise Exception('All inputs in a list must have the same size')

    def _cross_check(self):
        if self.is_data_list:
            n_data = self.data[0].shape[0]
        else:
            n_data = self.data.shape[0]

        if self.is_target_list:
            n_target = self.target[0].shape[0]
        else:
            n_target = self.target.shape[0]
        if n_target != n_data:
            raise Exception('target and data must have the same size')
        return n_target

    @staticmethod
    def _set_k_size(k_size, size):
        if k_size == 1:
            return size
        else:
            return np.floor(size / k_size).astype('int32')

    @staticmethod
    def get_data_slice(data, is_list, index):
        if not is_list:
            return data[index, :]
        else:
            return [d[index, :] for d in data]

    def get_fold_indexer(self):
        return range(self.k_size)

    def set_k_size(self, k_size):
        return CrossValidation(self.data, self.target, self.rmf, k_size)

    def get_fold(self):
        print("Running Folder" + str(self.fi))
        index_full = np.asarray(range(self.size))
        index_test = np.asarray(range(self.fs * self.fi, self.fs * (self.fi + 1)))
        index_train = np.where(np.logical_or(index_full > max(index_test), index_full < min(index_test)))[0]

        data_training = self.get_data_slice(self.data, self.is_data_list, index_train)
        data_validation = self.get_data_slice(self.data, self.is_data_list, index_test)
        target_training = self.get_data_slice(self.target, self.is_target_list, index_train)
        target_validation = self.get_data_slice(self.target, self.is_target_list, index_test)

        return data_training, target_training, data_validation, target_validation

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
