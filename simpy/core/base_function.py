import inspect

 
def build_function_input_dict(input_function, param_dict):
    if not callable(input_function):
        raise Exception('input must be a function')
    if not isinstance(param_dict, dict):
        raise Exception('input must be a dict')

    signature = inspect.signature(input_function)

    output_dict = {i: param_dict.get(i) for i in signature.parameters.keys() if param_dict.get(i) is not None}
    output_defulat = {i: signature.parameters.get(i).default for i in signature.parameters.keys() if
                      param_dict.get(i) is None}
    output_dict.update(output_defulat)
    if signature.parameters.__len__() != output_dict.__len__():
        missing_inputs = [i for i in signature.parameters.keys() if param_dict.get(i) is None]
        raise Exception('missing inputs:' + str(missing_inputs))
    return output_dict


def read_enum(input_enum, config_dict):
    enum_list = [k for k, e in config_dict.items() if e == input_enum.__name__]
    if enum_list.__len__() == 0:
        raise Exception('cant find enum value')
    try:
        return [input_enum[e] for e in enum_list]
    except KeyError:
        raise Exception('input to enum cant be found')
