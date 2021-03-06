import numpy as np
from .data import Data


class DataWrapper(object):
    def __init__(self, data_set_list, batch_size, shuffle_index=None):
        assert isinstance(data_set_list, list)
        for ds in data_set_list:
            assert isinstance(ds, Data)
        data_size = np.unique([ds.get_n_samples() for ds in data_set_list])
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

    def get_number_of_samples(self):
        return len(self.si)

    def shuffle(self):
        np.random.shuffle(self.si)
        return DataWrapper(self.dsl, self.batch_size, self.si)

    def __iter__(self):
        return self

    def __next__(self):  # Python 3: def __next__(self)
        if self.counter >= self.max_iteration:
            self.reset_counter()
            raise StopIteration
        else:
            start_point = self.counter * self.batch_size
            self.counter += 1
            index = np.linspace(start_point, start_point + self.batch_size - 1, self.batch_size).astype('int')
            index = index[index < self.n]
            return [ds.get_data(self.si[index]) for ds in self.dsl]

    def get_data_size(self):
        return [d.get_data_size() for d in self.dsl]

    def change_batch_size(self, batch_size):
        return DataWrapper(self.dsl, batch_size, shuffle_index=self.si)

    def change_shuffle_index(self, shuffle_index):
        return DataWrapper(self.dsl, self.batch_size, self.si)

    def split(self, split_size_list):
        split_size = np.asarray(split_size_list) * self.n
        split_size = np.insert(split_size, 0, 0)
        cum_sum_split_list = np.cumsum(split_size).astype('int')
        cum_sum_split_list[-1] = self.n
        return [
            DataWrapper([ds.reindex_data(self.si[cum_sum_split_list[i]:cum_sum_split_list[i + 1]]) for ds in self.dsl],
                        self.batch_size) for i, _ in enumerate(cum_sum_split_list[:-1])]

    def cycle_shift(self, shift_size):
        return DataWrapper(self.dsl, self.batch_size, shuffle_index=np.roll(self.si, shift_size))

    def merge(self, input_wrapper):
        if len(self.dsl) != len(input_wrapper.dsl): raise Exception('cant merge wrapper with difference size')
        dsl = [i.merge(j) for i, j in zip(self.dsl, input_wrapper.dsl)]
        return DataWrapper(dsl, self.batch_size)
