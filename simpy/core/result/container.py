class Result(object):
    def __init__(self, test_case, *args):
        self.test_case = test_case
        if args.__len__() == 0:
            raise Exception('result cant be empty args')
        elif args.__len__() % 2 != 0:
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
