import simpy
import numpy as np
import pickle


class Result(object):
    def __init__(self, test_case, *args):
        self.test_case = test_case
        if len(args) == 0:
            raise Exception('result cant be empty args')
        elif len(args) % 2 != 0:
            raise Exception('result args must be even number')
        else:
            result = dict()
            for i in range(round(args.__len__())):
                if i % 2 == 0:
                    name = args[i]
                    if not isinstance(name, str):
                        raise Exception('first input in a couple must be string')
                if i % 2 == 1:
                    if result.get(name) is None:
                        result.update({name: args[i]})
                    else:
                        raise Exception('result all ready exists')
            self.result = result

    def has_same_param(self, result):
        return self.test_case.has_same_param(result.test_case)

    def get_result(self, name):
        res = self.result.get(name)
        if res is None:
            raise Exception('result name:' + name + 'does not exists')
        return res

    def get_test_name(self):
        return self.test_case.get_name()

    def get_result_dict(self):
        return self.result


class ResultContainer(object):
    def __init__(self, global_params, test_result=[]):
        self.global_params = global_params
        self.test_result = test_result
        self.current = 0

    def clear(self):
        self.test_result.clear()

    def is_empty(self):
        return self.test_result.__len__() == 0

    def add_result(self, result):
        if not isinstance(result, Result):
            raise Exception('input must be of type result')
        self.test_result.append(result)

    def __iter__(self):
        return self

    def __next__(self):  # Python 3: def __next__(self)
        if self.current >= self.test_result.__len__():
            raise StopIteration
        else:
            test_result = self.test_result[self.current]
            self.current += 1
            return test_result

    def reset_iterator(self):
        self.current = 0

    def recreate_iterator(self):
        return ResultContainer(self.global_params, self.test_result)

    def get_test_cases(self):
        return [i.test_case for i in self.test_result]

    def __build_result__(self):
        result_dict_list = []
        test_list = []
        for r in self.recreate_iterator():
            result_dict_list.append(r.get_result_dict())
            test_list.append(r.get_test_name())
        return result_dict_list, test_list

    def plot_result(self, plot_cfg_list, save=None):
        """
        This function get a list of plot configs and plot them on the same figure
        :param plot_cfg_list:List of plot config
        :param save:None or str of path
        :return: Nothing
        """
        assert isinstance(plot_cfg_list, list)
        assert np.all([isinstance(plot_cfg, simpy.PlotConfiguration) for plot_cfg in plot_cfg_list])
        result_dict_list, test_list = self.__build_result__()
        [plot_cfg.plot_multiple_result(result_dict_list, test_list, True, save=save) for plot_cfg in plot_cfg_list]

    def print_summary(self, data_post_processing, save=None):
        result_dict_list, test_list = self.__build_result__()
        output_str = self.summary_function(data_post_processing, result_dict_list, test_list)
        print(output_str)
        if save is not None:
            text_file = open(save, "w")
            text_file.write(output_str)
            text_file.close()
            print("Saving summary to file:" + save)

    @staticmethod
    def summary_function(data_post_processing, result_dict_list, test_list):
        output_str = ''
        for tn, rd in zip(test_list, result_dict_list):
            output_str = output_str + tn + '[ '
            for m, pf in data_post_processing.items():
                output_str = output_str + m + ':' + str(pf(rd.get(m))) + ' '
            output_str = output_str + ' ]' + "\n"
        return output_str

    @staticmethod
    def loader(file_path):
        res = pickle.load(open(file_path, "rb"))
        if not isinstance(res, ResultContainer): raise Exception('the loaded pickle is not a of type result container')
        return res

    def saver(self, file_path):
        pickle.dump(self, open(file_path, "wb"))
