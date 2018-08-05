import numpy as np
from matplotlib import pyplot as plt


class PlotConfiguration(object):
    def __init__(self, x_subplot, y_subplot, *args, titles=None, x_labels=None, y_labels=None,
                 data_post_processing=None):
        assert isinstance(x_subplot, int)
        assert isinstance(y_subplot, int)
        self.n_plots = 1 if x_subplot == 1 and y_subplot == 1 else x_subplot * y_subplot
        assert len(args) <= self.n_plots
        assert titles is None or len(titles) == len(args)
        assert x_labels is None or len(x_labels) == len(args)
        assert y_labels is None or len(y_labels) == len(args)
        self.data_name = args
        self.x_subplot = x_subplot
        self.y_subplot = y_subplot
        self.is_single = np.all([len(a) == 1 for a in args])
        self.titles = titles
        self.x_labels = x_labels
        self.y_labels = y_labels
        self.is_titles = titles is not None
        self.is_x_labels = x_labels is not None
        self.is_y_labels = y_labels is not None
        self.is_dpp = data_post_processing is not None
        self.dpp = data_post_processing

    def plot_result(self, result_dict):
        assert isinstance(result_dict, dict)
        self.plot_multiple_result([result_dict], [], False)

    def plot_multiple_result(self, result_dict_list, tests_list, is_test_name=True, save=None):
        assert isinstance(result_dict_list, list)
        assert isinstance(tests_list, list)
        for i, dn in enumerate(self.data_name):
            if self.n_plots > 1: plt.subplot(self.x_subplot, self.y_subplot, i + 1)
            for d in dn:
                for ti, fg in enumerate([rdl.get(d) for rdl in result_dict_list]):
                    assert (self.dpp is not None and self.dpp.get(d) is not None) or fg is not None
                    if self.is_dpp and self.dpp.get(d) is not None:  # run data post processing
                        fg = self.dpp.get(d)(result_dict_list[ti])
                    if is_test_name and self.is_single:
                        plt.plot(fg, label=tests_list[ti])
                    elif is_test_name:
                        plt.plot(fg, label='Test Name:' + tests_list[ti] + ' Result Name:' + d)
                    elif self.is_single:
                        plt.plot(fg)
                    else:
                        plt.plot(fg, label=d)

                if self.is_single:
                    plt.title(d)
            if self.is_titles and not self.is_single:
                plt.title(self.titles[i])
            if self.is_x_labels:
                plt.xlabel(self.x_labels[i])
            if self.is_y_labels:
                plt.ylabel(self.y_labels[i])
            plt.legend()
            plt.grid()
        if save is not None:
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(12, 12)
            plt.savefig(save, dpi=100)
        else:
            plt.show()
