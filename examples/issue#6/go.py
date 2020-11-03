from goinpy import *

lib = load_go_lib('go.so')

golang_sort = setup_go_func(lib.GolangSort, [intGoSlice], intGoSlice)

golang_list = list_to_slice([intGo(i) for i in [1, 2, 3, 4, 5]])

golang_list = slice_to_list(golang_sort(golang_list))

print('Done?')
