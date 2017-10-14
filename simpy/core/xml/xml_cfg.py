from .xml_read import read_xml
from simpy.core.tests_configuration import TestConfiguration, TestsRunner


def __read_name__(xml_tree):
    name = xml_tree.get_tree_attr_by_key('name')
    if name is None:
        raise Exception('missing param name')
    return name


def __read_boolean_param__(param):
    return param == 'True' or param == '1'


def __param_reader__(xml_tree):
    param_type = xml_tree.get_tree_attr_by_key('type')
    param_value = xml_tree.get_tree_attr_by_key('value')
    if param_type is None:
        raise Exception('missing param type')
    if param_value is None:
        raise Exception('missing param value')
    if param_type == 'int':
        return int(param_value)
    elif param_type == 'float':
        return float(param_value)
    elif param_type == 'str':
        return param_value
    elif param_type == 'boolean':
        return __read_boolean_param__(param_value)
    elif param_type == 'enum':
        return param_value
    else:
        raise Exception('unknown type:' + param_type)


def __params_reader__(xml_tree):
    return {__read_name__(p): __param_reader__(p) for p in xml_tree.get_sub_trees('param')}


def __read_global_params__(xml_tree):
    sub_tree = xml_tree.get_sub_trees('global_params')
    if sub_tree.__len__() == 0:
        return dict()
    elif sub_tree.__len__() == 1:
        return __params_reader__(sub_tree[0])
    else:
        raise Exception('simulation can have only a single global params')
    return 0


def __read_single_param_cfg__(xml_tree, param_configs_dict):
    link_params = xml_tree.get_sub_trees('link_param')
    if link_params.__len__() == 0:
        return __params_reader__(xml_tree), True
    else:
        status = True
        for lp in link_params:
            status = status and (param_configs_dict.get(__read_name__(lp)) is not None)
        if status:
            param_cfg = param_configs_dict.get(__read_name__(lp)).copy()
            param_cfg.update(__params_reader__(xml_tree))
            return param_cfg, True
    return None, False


def __read_param_cfg__(xml_tree):
    sub_tree = xml_tree.get_sub_trees('parameter_configs')
    if sub_tree.__len__() == 0:
        return dict()
    elif sub_tree.__len__() == 1:
        param_cfg_list = sub_tree[0].get_sub_trees('param_cfg')
        status = {__read_name__(pc): True for pc in param_cfg_list}
        param_configs_dict = dict()
        counter = 0
        while counter != status.__len__():
            start_counter = counter
            for pc in param_cfg_list:
                current_cfg_name = __read_name__(pc)
                if status.get(current_cfg_name):
                    config, single_statue = __read_single_param_cfg__(pc, param_configs_dict)
                    if single_statue:
                        param_configs_dict.update({current_cfg_name: config})
                        status.update({current_cfg_name: False})
                        counter += 1
            if counter == start_counter:
                raise Exception('error in parsing configuration')
        return param_configs_dict
    else:
        raise Exception('simulation can have only a single parameter configs')


def __read_single_test__(xml_tree):
    test_name = __read_name__(xml_tree)
    param_cfg = xml_tree.get_tree_attr_by_key('param_cfg')
    enable = __read_boolean_param__(xml_tree.get_tree_attr_by_key('enable'))
    overwrite = __params_reader__(xml_tree)
    return TestConfiguration(test_name, enable, param_cfg, overwrite)


def __read_tests__(xml_tree):
    sub_tree = xml_tree.get_sub_trees('tests')
    if sub_tree.__len__() == 0:
        raise Exception('simulation must have single tests config')
    elif sub_tree.__len__() == 1:
        return [__read_single_test__(t) for t in sub_tree[0].get_sub_trees('test')]
    else:
        raise Exception('simulation can have only a single tests config')


def read_from_xml(xml_file_path):
    tree = read_xml(xml_file_path)
    global_param = __read_global_params__(tree)
    param_configs = __read_param_cfg__(tree)
    test_list = __read_tests__(tree)
    return TestsRunner(test_list, global_param, param_configs)
