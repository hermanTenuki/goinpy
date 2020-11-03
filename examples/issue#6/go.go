package main

import (
    "fmt"
    "C"
    "math/rand"
)

func quickSort(s []int) []int {

    if len(s) <= 1{
        return s
    }

    mark := s[rand.Intn(len(s))]
    var lowPart []int
    var midPart []int
    var hihPart []int

    for _, x :=range s{
        switch  {
        case  x < mark:
            lowPart = append(lowPart, x)
        case x == mark:
            midPart = append(midPart, x)
        case x > mark:
            hihPart = append(hihPart, x)
        }
    }

    lowPart = quickSort(lowPart)
    hihPart = quickSort(hihPart)

    var res []int
    res = append(lowPart, midPart...)
    res = append(res, hihPart...)

    return res
}

//export GolangSort
func GolangSort(s []int) []int {
    fmt.Println("I'm in")
    res := quickSort(s)
    fmt.Println("Got result, returning...")
    return res
}

func main() {}
