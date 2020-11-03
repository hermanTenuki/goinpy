import ctypes

intGo = ctypes.c_longlong
floatGo = ctypes.c_double
stringGo = ctypes.c_char_p
boolGo = ctypes.c_bool


class intGoSlice(ctypes.Structure):
    """
    Golang slice structure for intGo type
    """
    _fields_ = [("data", ctypes.POINTER(intGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class floatGoSlice(ctypes.Structure):
    """
    Golang slice structure for floatGo type
    """
    _fields_ = [("data", ctypes.POINTER(floatGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class stringGoSlice(ctypes.Structure):
    """
    Golang slice structure for stringGo type
    """
    _fields_ = [("data", ctypes.POINTER(stringGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


class boolGoSlice(ctypes.Structure):
    """
    Golang slice structure for boolGo type
    """
    _fields_ = [("data", ctypes.POINTER(boolGo)),
                ("len", ctypes.c_longlong),
                ("cap", ctypes.c_longlong)]


def load_go_lib(path: str) -> ctypes.CDLL:
    """
    Loads compiled Go library.
    :param path: Path to compiled Go library.
    :return: Library object.
    """
    return ctypes.cdll.LoadLibrary(path)


def setup_go_func(func, arg_types=None, res_type=None):
    """
    Set up Go function, so it know what types it should take and return.
    :param func: Specify Go function from library.
    :param arg_types: List containing file types that function is taking. Default: None.
    :param res_type: File type that function is returning. Default: None.
    :return: Returns func arg back for cases when you want to setup function and assign it to variable in one line.
    """
    if arg_types is not None:
        func.argtypes = arg_types
    if res_type is not None:
        func.restype = res_type
    return func


def str_to_go(string: str) -> str:
    """
    Convert Python str to Golang string.
    :param string: Python str.
    :return: Golang string.
    """
    return stringGo(bytes(string, encoding='UTF-8'))


def str_to_py(string) -> str:
    """
    Convert Golang string to Python str.
    :param string: Golang string.
    :return: Python str.
    """
    if type(string) == ctypes.c_char_p:
        string = string.value
    return string.decode('UTF-8')


def list_to_slice(ls: list, data_type=None) -> ctypes.Structure:
    """
    Convert Python list to Golang slice.
    :param ls: Python list.
    :param data_type: What data type this slice should store. For non-empty list, you can skip this parameter. Default: None.
    :return: Golang slice.
    """
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
    """
    Convert Golang slice to Python list.
    :param slc: Golang slice.
    :return: Python list.
    """
    ls = []
    for i in range(slc.len):
        ls.append(slc.data[i])
    return ls
