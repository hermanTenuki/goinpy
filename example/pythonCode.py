# Importing all from "goinpy" module
from goinpy import *

# Loading compiled .so library (compile command is in "golangCode.go")
golangLib = load_go_lib('golangCode.so')

# Integer example
setup_go_func(golangLib.TestInt, [intGo], intGo)  # Set "TestInt" func with "intGo" input and "intGo" output
inp = intGo(5)
res = golangLib.TestInt(inp)
print(f'Integer example:\n{inp} * 5 -> {res}\n')

# Float example
setup_go_func(golangLib.TestFloat, [floatGo], floatGo)  # Set "TestFloat" func with "floatGo" input and "floatGo" output
inp = floatGo(12.2)
res = golangLib.TestFloat(inp)
print(f'Float example:\n{inp} / 2 -> {res}\n')

# String example
setup_go_func(golangLib.TestString, [stringGo], stringGo)  # Set "TestString" func with "stringGo" input and "stringGo" output
inp = str_to_go('World')  # str_to_go(string) - convert python string to golang string
res = str_to_py(golangLib.TestString(inp))  # str_to_py(string) - convert golang string to python string
print(f'String example:\n{inp} -> {res}\n')

# Slice example
setup_go_func(golangLib.TestSlice, [sliceGo], sliceGo)  # Set "TestSlice" func with "sliceGo" input and "sliceGo" output
inp = [intGo(123), intGo(456)]  # Slice is containing "intGo" type. ONLY ONE TYPE ALLOWED AT A TIME!
res = slice_to_list(  # slice_to_list - convert golang slice to python list
    golangLib.TestSlice(list_to_slice(inp, intGo))
)
print(f'Slice (list) example:\n{inp} -> {res}\n')
