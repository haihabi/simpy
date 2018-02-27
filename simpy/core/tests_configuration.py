from .base_function import read_enum, build_function_input_dict
from simpy.core.result.container import ResultContainer, Result


class TestConfiguration(object):
    def __init__(self, name, enable, config_name, overwrite):
        if not isinstance(enable, bool):
            raise Exception('enable must be a boolean')
        self.name = name
        self.enable = enable
        self.config_name = config_name
        self.overwrite = overwrite

    def enable_test(self):
        self.enable = True


class Test(object):
    def __init__(self, test_config, param_config):
        self.test_config = test_config
        # overwrite params
        param_config = param_config.copy()  # create a clean copy of params
        param_config.update(test_config.overwrite)  # perform overwrite
        self.param_config = param_config

    def get_name(self):
        return self.test_config.name

    def get_param(self, name):
        return self.param_config.get(name)

    def get_params(self):
        return self.param_config

    def read_enum(self, input_enum):
        return read_enum(input_enum, self.param_config)

    def run_function_from_test(self, input_function):
        function_inputs = build_function_input_dict(input_function, self.param_config)
        return input_function(**function_inputs)

    def generate_test_result(self, *args):
        return Result(self, *args)

    def has_same_param(self, input_test):
        if input_test.param_config.__len__() != self.param_config.__len__():
            return False
        for k in input_test.param_config.keys():
            if self.param_config.get(k) is None:
                return False
        return True


class TestsRunner(object):
    def __init__(self, test_list, global_param, param_configurations):
        self.test_list = test_list
        self.global_param = global_param
        self.param_configurations = param_configurations
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):  # Python 3: def __next__(self)
        if self.current >= self.test_list.__len__():
            raise StopIteration
        else:
            while True:
                if self.test_list[self.current].enable:
                    tc = self.test_list[self.current]
                    if self.param_configurations.get(tc.config_name) is None:
                        raise Exception('cant find param config')
                    t = Test(tc, self.param_configurations.get(tc.config_name))
                    print("Running Test:" + t.get_name())
                    self.current += 1
                    return t
                self.current += 1
                if self.current >= self.test_list.__len__():
                    raise StopIteration

    next = __next__  # Python 2

    def get_global_param(self, param_name):
        return self.global_param.get(param_name)

    def generate_result_container(self):
        return ResultContainer(self.global_param)

    def run_function_from_global(self, input_function):
        function_inputs = build_function_input_dict(input_function, self.global_param)
        return input_function(**function_inputs)

    def generate_test_iterator(self):
        return TestsRunner(self.test_list, self.global_param, self.param_configurations)
