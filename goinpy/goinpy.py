import ctypes

intGo = ctypes.c_longlong
floatGo = ctypes.c_double
stringGo = ctypes.c_char_p
boolGo = ctypes.c_bool


class intGoSlice(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(intGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class floatGoSlice(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(floatGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class stringGoSlice(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(stringGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class boolGoSlice(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(boolGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


def load_go_lib(path: str) -> ctypes.CDLL:
    return ctypes.cdll.LoadLibrary(path)


def setup_go_func(func, arg_types=None, res_type=None):
    if arg_types is not None:
        func.argtypes = arg_types
    if res_type is not None:
        func.restype = res_type


def str_to_go(string: str) -> str:
    return stringGo(bytes(string, encoding='UTF-8'))


def str_to_py(string) -> str:
    if type(string) == ctypes.c_char_p:
        string = string.value
    return string.decode('UTF-8')


def list_to_slice(ls: list, data_type=None) -> ctypes.Structure:
    length = len(ls)
    if data_type is None:
        if length > 0:
            data_type = type(ls[0])
        else:
            raise AttributeError('Specify data_type for empty slice')

    kwargs = {
        'data': (data_type * length)(*ls),
        'len': length,
        'cap': length
    }

    if data_type == intGo:
        slc = intGoSlice(**kwargs)
    elif data_type == floatGo:
        slc = floatGoSlice(**kwargs)
    elif data_type == stringGo:
        slc = stringGoSlice(**kwargs)
    elif data_type == boolGo:
        slc = boolGoSlice(**kwargs)
    else:
        raise AttributeError('Your data_type is not supported, choose any of xGo variables')
    return slc


def slice_to_list(slc) -> list:
    ls = []
    for i in range(slc.len):
        ls.append(slc.data[i])
    return ls
