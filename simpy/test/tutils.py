'''
Created on Oct 14, 2017

@author: haih
'''
import os
import inspect

def get_current_folder_path():
    return os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
