package hello

import (
	"fmt"
)

import "rsc.io/quote"

func Hello() {
	fmt.Println("你好 👋")
}

func main() {
	fmt.Println(quote.Go())
}
