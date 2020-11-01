import ctypes

intGo = ctypes.c_longlong
floatGo = ctypes.c_double
stringGo = ctypes.c_char_p


def load_go_lib(path: str) -> ctypes.CDLL:
    return ctypes.cdll.LoadLibrary(path)


def setup_go_func(func, argtypes=None, restype=None):
    if argtypes is not None:
        func.argtypes = argtypes
    if restype is not None:
        func.restype = restype


class sliceGo(ctypes.Structure):
    pass


def list_to_slice(ls: list, data_type) -> sliceGo:
    length = len(ls)
    sliceGo._fields_ = [("data", ctypes.POINTER(data_type)),
                        ("len", ctypes.c_longlong), ("cap", ctypes.c_longlong)]
    return sliceGo(data=(data_type * length)(*ls), len=length, cap=length, data_type=data_type)


def str_to_go(string: str) -> str:
    return stringGo(bytes(string, encoding='UTF-8'))


def str_to_py(string: str) -> str:
    return string.decode('UTF-8')


def slice_to_list(slice) -> list:
    ls = []
    for i in range(slice.len):
        ls.append(slice.data[i])
    return ls
