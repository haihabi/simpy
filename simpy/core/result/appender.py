import simpy


class ResultAppender(object):
    def __init__(self, result_list, record_function_dict={}, result_function_dict={}, result_not2print=None):
        self.result_list = result_list
        self.result_dict = {r: [] for r in self.result_list}  # init result dict
        self.record_dict = {r: [] for r in self.result_list}  # init result dict
        self.manual_result = {}
        self.record_function_dict = record_function_dict
        self.result_function_dict = result_function_dict
        self.rn2p = result_not2print

    def update_result(self, result_dict):
        for k, r in result_dict.items():
            if self.result_dict.get(k) is None:
                raise Exception('update undefined result')
            else:
                res = self._get_result_function(k)(result_dict.get(k))
                self.result_dict.get(k).append(res)

    def _get_result_function(self, k):
        func = self.result_function_dict.get(k)
        if func is None:
            func = simpy.data_identity
        return func

    def __clear_result__(self):
        self.result_dict = {r: [] for r in self.result_list}  # init result dict

    def clear_record(self):
        self.record_dict = {r: [] for r in self.result_list}

    def _get_record_function(self, k):
        func = self.record_function_dict.get(k)
        if func is None:
            func = simpy.data_mean
        return func

    def update_record(self):
        [self.record_dict.get(k).append(self._get_record_function(k)(self.result_dict.get(k))) for k in
         self.result_list if self.result_dict.get(k).__len__() > 0]
        self.__clear_result__()

    def get_record(self, record_name=None):
        if record_name is None:
            return self.record_dict
        else:
            if self.manual_result.get(record_name) is not None:
                return self.manual_result.get(record_name)
            return self.record_dict.get(record_name)

    def print_record(self):
        str_output = ''
        for k, v in self.get_record().items():
            if (self.rn2p is None or k not in self.rn2p) and len(v) > 0:
                str_output = str_output + "\n" + k + ':' + str(v[-1])
        print(str_output)

    def add_manual_result(self, result):
        self.manual_result.update(result)
