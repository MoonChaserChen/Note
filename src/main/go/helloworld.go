package main

import "fmt"

func init() {
	fmt.Printf("init method\n")
}

func add(a, b int) int {
	return a + b
}

func main() {
	var oneStr string = "abc"
	anotherStr := "def"
	fmt.Println("oneStr:", oneStr)
	fmt.Printf("anotherStr:%s\n", anotherStr)
	fmt.Println("a+b=", add(1, 3))
	fmt.Printf("a+b=%d\n", add(1, 3))
	print(13 / 2)
}
