from matplotlib import pyplot as plt


class PlotConfiguration(object):
    def __init__(self, x_subplot, y_subplot, *args):
        assert isinstance(x_subplot, int)
        assert isinstance(y_subplot, int)
        self.n_plots = 1 if x_subplot == 1 and y_subplot == 1 else x_subplot * y_subplot
        assert len(args) <= self.n_plots
        self.data_name = args

    def plot_result(self, result_dict):
        for i, dn in enumerate(self.data_name):
            if self.n_plots > 1: plt.subplot(self.x_subplot, self.y_subplot, i + 1)
            for d in dn:
                data = result_dict.get(d)
                if data is None:
                    raise Exception('cant find data named:' + d)
                plt.plot(data)
        plt.show()
