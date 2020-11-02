import ctypes

intGo = ctypes.c_longlong
floatGo = ctypes.c_double
stringGo = ctypes.c_char_p
boolGo = ctypes.c_bool


def load_go_lib(path: str) -> ctypes.CDLL:
    return ctypes.cdll.LoadLibrary(path)


def setup_go_func(func, arg_types=None, res_type=None):
    if arg_types is not None:
        func.argtypes = arg_types
    if res_type is not None:
        func.restype = res_type


class sliceGo(ctypes.Structure):
    pass


def list_to_slice(ls: list, data_type=None) -> sliceGo:
    length = len(ls)
    if data_type is None:
        if length > 0:
            data_type = type(ls[0])
        else:
            raise AttributeError('Specify data_type for empty slice')
    sliceGo._fields_ = [("data", ctypes.POINTER(data_type)),
                        ("len", ctypes.c_longlong), ("cap", ctypes.c_longlong)]
    return sliceGo(data=(data_type * length)(*ls), len=length, cap=length, data_type=data_type)


def slice_to_list(slice: sliceGo) -> list:
    ls = []
    for i in range(slice.len):
        ls.append(slice.data[i])
    return ls


def str_to_go(string: str) -> str:
    return stringGo(bytes(string, encoding='UTF-8'))


def str_to_py(string: bytes) -> str:
    return string.decode('UTF-8')
