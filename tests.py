from goinpy import *
import unittest
import ctypes


class TestLoadGoLib(unittest.TestCase):
    def test_success(self):
        lib = load_go_lib('golangCode.so')
        self.assertEqual(type(lib), ctypes.CDLL)

    def test_wrong(self):
        with self.assertRaises(OSError):
            lib = load_go_lib('wrongfile.qwe')


class TestVariablesConversion(unittest.TestCase):

    def test_int(self):
        inp = 10
        conv = intGo(inp)
        self.assertEqual(type(conv), ctypes.c_longlong)
        res = conv.value
        self.assertEqual(res, inp)

    def test_float(self):
        inp = 12.2
        conv = floatGo(inp)
        self.assertEqual(type(conv), ctypes.c_double)
        res = conv.value
        self.assertEqual(res, inp)

    def test_string(self):
        inp = 'This is a string'
        conv = str_to_go(inp)
        self.assertEqual(type(conv), ctypes.c_char_p)
        res = str_to_py(conv)
        self.assertEqual(res, inp)

    def test_slice(self):
        numbers = [123, 456, 789]
        inp = [intGo(i) for i in numbers]
        conv = list_to_slice(inp, intGo)
        self.assertEqual(type(conv), intGoSlice)
        res = slice_to_list(conv)
        self.assertEqual(res, numbers)

    def test_bool(self):
        inp = False
        conv = boolGo(inp)
        self.assertEqual(type(conv), ctypes.c_bool)
        res = conv.value
        self.assertEqual(res, inp)


class TestListsSlices(unittest.TestCase):
    def test_empty_list(self):
        """
        Empty list to slice should work but only with specified type
        """
        inp = []
        with self.assertRaises(AttributeError):
            conv = list_to_slice(inp)
        conv = list_to_slice(inp, boolGo)
        self.assertEqual(type(conv), boolGoSlice)
        res = slice_to_list(conv)
        self.assertEqual(res, inp)

    # # https://github.com/hermanTenuki/goinpy/issues/3
    # def test_lists_in_list(self):
    #     """
    #     Testing lists inside a list
    #     """
    #     list1 = list_to_slice([intGo(i) for i in [1, 2, 3]])
    #     list2 = list_to_slice([intGo(i) for i in [4, 5, 6]])
    #     ls = list_to_slice([list1, list2])
    #     ls_back = slice_to_list(ls)
    #     list1_back = slice_to_list(ls_back[0])

    def test_filled_list(self):
        numbers = [123, 456, 789]
        inp = [intGo(i) for i in numbers]
        conv = list_to_slice(inp, intGo)
        self.assertEqual(type(conv), intGoSlice)
        res = slice_to_list(conv)
        self.assertEqual(res, numbers)
        # Without specifying file_type
        conv = list_to_slice(inp)
        self.assertEqual(type(conv), intGoSlice)
        res = slice_to_list(conv)
        self.assertEqual(res, numbers)

    def test_wrong_file_types(self):
        """
        Slice can contain only one file_type at a time
        """
        inp = [intGo(1), boolGo(True), str_to_go('Hi')]
        with self.assertRaises(TypeError):
            conv = list_to_slice(inp)


class TestSetupGoFunc(unittest.TestCase):
    def setUp(self):
        self.lib = load_go_lib('examples/golangCode.so')

    def test_without_setup(self):
        """
        If we don't set up input and output file types for functions, they will be converted to unexpected types
        """
        inp = False
        conv = boolGo(inp)
        res = self.lib.TestBool(conv)
        self.assertNotEqual(type(res), bool)

    def test_with_only_input_setup(self):
        """
        If we only set up input file type, it will work okay on golang side, but we will still get wrong result
        """
        setup_go_func(self.lib.TestBool, [boolGo])
        inp = False
        conv = boolGo(inp)
        res = self.lib.TestBool(conv)
        self.assertNotEqual(type(res), bool)

    def test_with_full_setup(self):
        """
        If input and output file types are set correct, final result should be as expected
        """
        setup_go_func(self.lib.TestBool, [boolGo], boolGo)
        inp = False
        conv = boolGo(inp)
        res = self.lib.TestBool(conv)
        self.assertEqual(type(res), bool)


class TestGolangIntegrationsExamples(unittest.TestCase):
    def setUp(self):
        self.lib = load_go_lib('examples/golangCode.so')

    def test_int(self):
        setup_go_func(self.lib.TestInt, [intGo, intGo], intGo)
        inp1, inp2 = 5, 10
        conv1, conv2 = intGo(inp1), intGo(inp2)
        res = self.lib.TestInt(conv1, conv2)
        self.assertEqual(type(res), int)
        self.assertEqual(res, inp1 + inp2)

    def test_float(self):
        setup_go_func(self.lib.TestFloat, [floatGo], floatGo)
        inp = 12.2
        conv = floatGo(inp)
        res = self.lib.TestFloat(conv)
        self.assertEqual(type(res), float)
        self.assertEqual(res, inp / 2)

    def test_string(self):
        setup_go_func(self.lib.TestString, [stringGo], stringGo)
        inp = 'World'
        conv = str_to_go(inp)
        res = self.lib.TestString(conv)
        resConv = str_to_py(res)
        self.assertEqual(type(resConv), str)
        self.assertEqual(resConv, 'Hello, World')

    def test_slice(self):
        setup_go_func(self.lib.TestSlice, [intGoSlice], intGoSlice)
        inp = [1, 2, 3]
        inpGo = [intGo(i) for i in inp]
        conv = list_to_slice(inpGo)
        res = self.lib.TestSlice(conv)
        resConv = slice_to_list(res)
        self.assertEqual(type(resConv), list)
        self.assertEqual(resConv, [666, 2, 3])

    def test_bool(self):
        setup_go_func(self.lib.TestBool, [boolGo], boolGo)
        inp = False
        conv = boolGo(inp)
        res = self.lib.TestBool(conv)
        self.assertEqual(type(res), bool)
        self.assertEqual(res, not inp)
        # Should also work without conversion to boolGo
        res = self.lib.TestBool(inp)
        self.assertEqual(type(res), bool)
        self.assertEqual(res, not inp)


if __name__ == '__main__':
    unittest.main()
