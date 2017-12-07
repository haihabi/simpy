class ResultAppender(object):
    def __init__(self, result_list, record_function_dict, result_function_dict):
        self.result_list = result_list
        self.result_dict = {r: [] for r in self.result_list}  # init result dict
        self.record_dict = {r: [] for r in self.result_list}  # init result dict
        self.record_function_dict = record_function_dict
        self.result_function_dict = result_function_dict

    def update_result(self, result_dict):
        for k, r in result_dict.items():
            if self.result_dict.get(k) is None:
                raise Exception('update undefined result')
            else:
                res = self.result_function_dict.get(k)(result_dict.get(k))
                self.result_dict.get(k).append(res)

    def __clear_result__(self):
        self.result_dict = {r: [] for r in self.result_list}  # init result dict

    def clear_record(self):
        self.record_dict = {r: [] for r in self.result_list}

    def update_record(self):
        [self.record_dict.get(k).append(self.record_function_dict.get(k)(self.result_dict.get(k))) for k in
         self.result_list if self.result_dict.get(k).__len__() > 0]
        self.__clear_result__()

    def get_record(self, record_name=None):
        if record_name is None:
            return self.record_dict
        else:
            return self.record_dict.get(record_name)
