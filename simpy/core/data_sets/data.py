import numpy as np


class Data(object):
    def __init__(self, data):
        assert isinstance(data, np.ndarray)
        self.data = data

    def shuffle(self, index):
        return Data(self.data[index, :])

    def get_data_size(self):
        return self.data.shape[0]

    def get_data(self, index=None):
        if index is None:
            return self.data
        else:
            return self.data[index, :]
