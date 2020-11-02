/*
command for building .so library:
    go build -o golangCode.so -buildmode=c-shared golangCode.go
                    ^                ^                ^
                    |                |                |
               output file           |                |
                            specify compiling to C    |
                                                 input file

*/

package main

import "C"
import (
    "fmt"
)

//export TestFunc
func TestFunc() {
    fmt.Println("Hello World!")
}

//export TestInt
func TestInt(x, y int) int {
    return x + y
}

//export TestFloat
func TestFloat(x float64) float64 {
    return x / 2
}

//export TestString
func TestString(x *C.char) *C.char {
    /*
    input and output strings should be "*C.char"
    you can convert C to golang string with "C.GoString(...)"
    you can convert golang to C string with "C.CString(...)"
    */
    str := C.GoString(x)
    newStringC := C.CString("Hello, " + str)
    return newStringC
}

//export TestSlice
func TestSlice(x []int) []int {
    x[0] = 666
    return x
}

//export TestBool
func TestBool(x bool) bool {
    return !(x)
}

func main() {

}
