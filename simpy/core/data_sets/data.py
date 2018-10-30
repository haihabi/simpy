import numpy as np


class Data(object):
    def __init__(self, data):
        assert isinstance(data, np.ndarray)
        self.data = data
        self.is_one_d = len(data.shape)

    def shuffle(self, index):
        return Data(self.data[index, :])

    def get_n_samples(self):
        return self.data.shape[0]

    def get_data(self, index=None):
        if index is None:
            return self.data
        else:
            if self.is_one_d:
                return self.data[index]
            return self.data[index, :]

    def get_data_size(self):
        if len(self.data.shape) > 1:
            return self.data.shape[1:]
        return 1

    def reindex_data(self, index):
        return Data(self.get_data(index))

    def merge(self, input_data):
        return Data(np.concatenate([self.data, input_data.data], axis=0))
