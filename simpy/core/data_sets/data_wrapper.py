import numpy as np
from dataset.data import Data


class DataWrapper(object):
    def __init__(self, data_set_list, batch_size, shuffle_index=None):
        assert isinstance(data_set_list, list)
        for ds in data_set_list:
            assert isinstance(ds, Data)
        data_size = np.unique([ds.get_data_size() for ds in data_set_list])
        assert len(data_size) == 1
        assert batch_size > 0
        self.n = data_size[0]
        self.batch_size = batch_size
        self.dsl = data_set_list
        self.counter = 0
        self.max_iteration = np.ceil(self.n / self.batch_size).astype('int')
        self.si = shuffle_index
        if shuffle_index is None:
            self.si = np.linspace(0, self.n - 1, self.n).astype('int')

    def reset_counter(self):
        self.counter = 0

    def shuffle(self):
        np.random.shuffle(self.si)
        return DataWrapper(self.dsl, self.batch_size, self.si)

    def __iter__(self):
        return self

    def __next__(self):  # Python 3: def __next__(self)
        if self.counter >= self.max_iteration:
            raise StopIteration
        else:
            start_point = self.counter * self.batch_size
            self.counter += 1
            index = np.mod(np.linspace(start_point, start_point + self.batch_size - 1, self.batch_size).astype('int'),
                           self.n)
            return [ds.get_data(self.si[index]) for ds in self.dsl]
