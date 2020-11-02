# Importing all from "goinpy" module
from goinpy import *

# Loading compiled .so library (compile command is in "golangCode.go")
golangLib = load_go_lib('golangCode.so')

# Hello World example
golangLib.TestFunc()
print('')  # \n

# Integer example
setup_go_func(golangLib.TestInt, [intGo, intGo], intGo)  # Set "TestInt" func with "intGo" inputs and "intGo" output
input_1 = intGo(5)
input_2 = intGo(10)
output_result = golangLib.TestInt(input_1, input_2)
print(f'Integer example:\n{input_1} + {input_2} -> {output_result}\n')

# Float example
setup_go_func(golangLib.TestFloat, [floatGo], floatGo)
input_data = floatGo(12.2)
output_result = golangLib.TestFloat(input_data)
print(f'Float example:\n{input_data} / 2 -> {output_result}\n')

# String example
setup_go_func(golangLib.TestString, [stringGo], stringGo)
input_data = str_to_go('World')  # str_to_go(string) - convert python string to golang string
output_result = str_to_py(golangLib.TestString(input_data))  # str_to_py(string) - convert golang string to python string
print(f'String example:\n{input_data} -> {output_result}\n')

# Slice example
setup_go_func(golangLib.TestSlice, [intGoSlice], intGoSlice)
input_list = [intGo(123), intGo(456)]  # Slice is containing "intGo" type. ONLY ONE TYPE ALLOWED AT A TIME!
input_data = list_to_slice(input_list, intGo)  # list_to_slice - convert python list to golang slice
output_result = slice_to_list(golangLib.TestSlice(input_data))  # slice_to_list - convert golang slice to python list
print(f'Slice (list) example:\n{input_data} -> {output_result}\n')

# Bool example
setup_go_func(golangLib.TestBool, [boolGo], boolGo)
input_data = False  # No need to convert python bool to boolGo (but if you want, you can do it)
output_result = golangLib.TestBool(input_data)
print(f'Bool example:\n{input_data} -> {output_result}\n')
