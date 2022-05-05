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
# Variable Table
# ====================
class Var_table:
    table = {}

    def __init__(self):
        self.table = dict()
    
    def add(self, var_name, var_type, var_scope, var_value):
        self.table[var_name] = { 'name' : var_name, 'type' : var_type, 'scope' : var_scope, 'value' : var_value }

    def search(self, var_name, var_scope):
        # If None then it does not exist in this var_table
        return self.table.get(var_name)

    def print(self):
        # print("======== VARIABLE TABLE ========")
        print ("|| {:<10} | {:<10} | {:<10} | {:<10} ||".format('Name', 'Type', 'Scope', 'Value'))
        for k,v in self.table.items():
            print("{:<52} || {:<10} | {:<10} | {:<10} | {:<10} ||".format('', k, v['type'], v['scope'], v['value']))
    
    def __del__(self):
        del self.table

# ====================
# Function Directory
# ====================
class Func_directory:
    func_directory = {}
    
    def __init__(self):
        self.func_directory = dict()
    
    def add_func(self, func_start, func_name, func_type):
        # Create its variable table
        var_table = Var_table()
        self.func_directory[func_name] = { 'start_address' : func_start, 'type' : func_type, 'vars_dir' : var_table }
    
    def search_func(self, func_name):
        # If None then it does not exist in func_directory
        return self.func_directory.get(func_name)

    def add_var(self, func_name, var_name, var_type, var_scope, var_value):
        # Add var to the var table corresponding to the specified func
        var_table = self.search_func(func_name)['vars_dir']
        var_table.add(var_name, var_type, var_scope, var_value)
    
    def search_var(self, func_name, var_name, var_scope):
        # Check if var exists in the var table corresponding to the specified func
        var_table = self.search_func(func_name)['vars_dir']
        return var_table.search(var_name, var_scope)

    def print(self):
        print("======== FUNCTION DIRECTORY ========")
        print ("{:<20} | {:<15} | {:<11} || {:<49} || ".format('Name','Start Address','Type', 'Vars'))
        for k,v in self.func_directory.items():
            print('------------------------------------------------------------------------------------------------------------')
            print("{:<20} | {:<15} | {:<10} ".format(k, v['start_address'], v['type']), end = ' ')
            v['vars_dir'].print()
            print()

    def __del__(self):
        del self.func_directory
    
# buffer = Func_directory()
# buffer.add_func(1, 'program', 'void')
# buffer.add_var('program', 'i', 'int', 'global', '10')
# buffer.add_func('45', 'hello', 'int')
# buffer.print()


