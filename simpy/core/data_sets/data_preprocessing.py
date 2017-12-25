import numpy as np


def data_shuffle_index(n):
    index = np.arange(n)
    np.random.shuffle(index)
    return index


def reformat_2d(data, target, num_labels):
    assert isinstance(data, np.ndarray)
    assert isinstance(target, np.ndarray)
    assert len(target.shape) == 3
    data_new = data.astype(np.float32)
    # Map 0 to [1.0, 0.0, 0.0 ...], 1 to [0.0, 1.0, 0.0 ...]
    labels = (np.arange(num_labels) == target[:, :, None]).astype(np.float32)
    return data_new, labels


def reformat_1d(data, target, num_labels):
    assert isinstance(data, np.ndarray)
    assert isinstance(target, np.ndarray)
    assert len(target.shape) == 2
    data_new = data.astype(np.float32)
    # Map 0 to [1.0, 0.0, 0.0 ...], 1 to [0.0, 1.0, 0.0 ...]
    labels = (np.arange(num_labels) == target[:, None]).astype(np.float32)
    return data_new, labels
