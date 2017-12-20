'''
Created on Nov 6, 2017

@author: haih
'''


def is_main(input_class):
    return str(input_class).__contains__("__main__")


def get_all_inheritors_of_main(input_class):
    subclasses = set()
    work = [input_class]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                if is_main(child):
                    subclasses.add(child)
                    work.append(child)
    return subclasses
