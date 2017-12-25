import numpy as np


def data_concat(result_a):
    return np.concatenate(result_a, axis=0)


def data_mean(result_a):
    return np.mean(result_a)


def data_identity(result_a):
    return result_a


def data_stack(result_a):
    return np.stack(result_a)


def data_single(result_a):
    return result_a[0]


def data_stack_mean(result_a):
    return np.mean(data_stack(result_a),axis=0)
