#
# @file utilis.py
# @author David Luna and Yulisa Medina
# @brief
# @version 0.1
# @date 2022-05-05
#
# @copyright Copyright (c) 2022
#
#

# ====================
# Function Directory
# ====================
class func_directory:
    table = {}
    
    def __init__(self):
        self.table = dict()
    
    def add(self, func_name, func_type, vars_dir):
        self.table[func_name] = { 'type' : func_type, 'vars_dir' : vars_dir }
    
    def search(self, func_name):
        # If None then it does not exist in func_directory
        return self.table.get(func_name)

    def __del__(self):
        del self.table


