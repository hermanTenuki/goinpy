# goinpy - Golang In Python

This is a python package, which is made to use Golang functions inside Python code more easily.

Embedding Golang functions in python can be very handy, for example, if you want to move some big computations from slow Python to faster Golang and immediately get a result back.

## Installation

You can install this package from PyPi with ```pip install goinpy```;

Then in python code, import it with ```from goinpy import *```.

## How to use

Most of these examples are represented in the [example folder](example/).

### Basic "Hello World!" example

#### Golang function export

Let's start with exporting a simple Golang "Hello World!" function.

```
package main

import (
    "C"
    "fmt"
)

//export TestFunc
func TestFunc() {
    fmt.Println("Hello World!")
}

func main() {

}
```

To export functions, we need to import ```"C"``` library, and specify by ```//export NAME``` comment, what function we need to export.
Also make sure ```func main() {}``` is exists.

#### Compiling to C

After we made the Golang file, for example, ```HelloWorld.go```, we need to compile it to C.
We can do it by typing ```go build -o HelloWorld.so -buildmode=c-shared HelloWorld.go``` in terminal.
This command is also represented in [example/golangCode.go](https://github.com/hermanTenuki/goinpy/tree/main/example).

If all is okay, we should now see three different files: ```HelloWorld.go```, ```HelloWorld.so```, ```HelloWorld.h```.
```.so``` is the compiled file that we need.

#### Call Golang function from Python

Let's create ```HelloWorld.py```.

```
from goinpy import *

golangLib = load_go_lib('HelloWorld.so')

golangLib.TestFunc()
```

Here we just imported all from ```goinpy``` package, loaded compiled C library into ```golangLib```, and called ```TestFunc``` function with it.

After running ```python HelloWorld.py``` in a terminal, the output should be ```Hello World!``` as expected.

### Advanced examples with different types

#### Integer example

```golangCode.go```:

```
//export TestInt
func TestInt(x, y int) int {
    return x + y
}
```

```pythonCode.py```:

```
setup_go_func(golangLib.TestInt, [intGo, intGo], intGo)
input_1 = intGo(5)
input_2 = intGo(10)
output_result = golangLib.TestInt(input_1, input_2)  # 15
```

Here we met 2 new functions:
- ```intGo(int)``` - convert python ```int``` to golang ```int```. You can convert it back by ```some_int.value```;
- ```setup_go_func(func, arg_types=None, res_type=None)``` - if Golang function is taking or returning some data, we need to setup this function.
First ```func``` arg is the function we are trying to setup.
Second ```arg_types``` arg is a list for types this function is waiting.
Third ```res_type``` arg is a type it's returning.

#### Float example

```golangCode.go```:

```
//export TestFloat
func TestFloat(x float64) float64 {
    return x / 2
}
```

```pythonCode.py```:

```
setup_go_func(golangLib.TestFloat, [floatGo], floatGo)
input_data = floatGo(12.2)
output_result = golangLib.TestFloat(input_data)  # 6.1
```

Here we met 1 new function:
- ```floatGo(float)``` - convert python ```float``` to golang ```float64```.

#### String example

```golangCode.go```:

```
//export TestString
func TestString(x *C.char) *C.char {
    str := C.GoString(x)
    newStringC := C.CString("Hello, " + str)
    return newStringC
}
```

Note that for strings, we need to use ```*C.char``` for in and out.
You can convert between this and normal string by using ```C.GoString(char)``` and ```C.CString(string)```.

```pythonCode.py```:

```
setup_go_func(golangLib.TestString, [stringGo], stringGo)
input_data = str_to_go('World')
output_result = str_to_py(golangLib.TestString(input_data))  # "Hello, World!"
```

Here we met 3 new functions:
- ```stringGo``` - golang ```string```;
- ```str_to_go(str)``` - convert python ```str``` to golang ```string```;
- ```str_to_py(string)``` - convert golang ```string``` to python ```str```.

#### Slice example

```golangCode.go```:

```
//export TestSlice
func TestSlice(x []int) []int {
    x[0] = 666
    return x
}
```

```pythonCode.py```:

```
setup_go_func(golangLib.TestSlice, [sliceGo], sliceGo)
input_list = [intGo(123), intGo(456)]
input_data = list_to_slice(input_list, intGo)
output_result = slice_to_list(golangLib.TestSlice(input_data))  # [666, 456]
```

Here we met 3 new functions:
- ```sliceGo``` - golang ```slice```;
- ```list_to_slice(list, data_type: None)``` - convert python ```list``` to golang ```slice```.
First arg is actual list we are converting.
Second ```data_type``` arg is what type this slice is storing (NOTE THAT SLICE CAN'T STORE DIFFERENT FILE TYPES AT ONCE).
- ```slice_to_list(slice)``` - convert golang ```slice``` to python ```list```.

#### Bool example

```golangCode.go```:

```
//export TestBool
func TestBool(x bool) bool {
    return !(x)
}
```

```pythonCode.py```:

```
setup_go_func(golangLib.TestBool, [boolGo], boolGo)
input_data = False
output_result = golangLib.TestBool(input_data)  # True
```

Here we met 1 new function:
- ```boolGo``` - golang ```bool```. No need in converting python bool to golang bool;
