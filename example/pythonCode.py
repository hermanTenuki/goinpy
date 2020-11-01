# Importing all from "goinpy" module
from goinpy import *

# Loading compiled .so library (compile command is in "golangCode.go")
golangLib = load_go_lib('golangCode.so')

# Integer example
setup_go_func(golangLib.TestInt, [intGo], intGo)  # Set "TestInt" func with "intGo" input and "intGo" output
input_data = intGo(5)
output_result = golangLib.TestInt(input_data)
print(f'Integer example:\n{input_data} * 5 -> {output_result}\n')

# Float example
setup_go_func(golangLib.TestFloat, [floatGo], floatGo)  # Set "TestFloat" func with "floatGo" input and "floatGo" output
input_data = floatGo(12.2)
output_result = golangLib.TestFloat(input_data)
print(f'Float example:\n{input_data} / 2 -> {output_result}\n')

# String example
setup_go_func(golangLib.TestString, [stringGo], stringGo)  # Set "TestString" func with "stringGo" input and "stringGo" output
input_data = str_to_go('World')  # str_to_go(string) - convert python string to golang string
output_result = str_to_py(golangLib.TestString(input_data))  # str_to_py(string) - convert golang string to python string
print(f'String example:\n{input_data} -> {output_result}\n')

# Slice example
setup_go_func(golangLib.TestSlice, [sliceGo], sliceGo)  # Set "TestSlice" func with "sliceGo" input and "sliceGo" output
input_list = [intGo(123), intGo(456)]  # Slice is containing "intGo" type. ONLY ONE TYPE ALLOWED AT A TIME!
input_data = list_to_slice(input_list, intGo)
output_result = slice_to_list(golangLib.TestSlice(input_data))  # slice_to_list - convert golang slice to python list
print(f'Slice (list) example:\n{input_data} -> {output_result}\n')
