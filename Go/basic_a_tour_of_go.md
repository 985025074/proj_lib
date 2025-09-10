# Go 语言

为什么药学go....

## package

导出包的规则  

只有大写开头才会导出

## 函数声明  

```go
package main


func test(x,y int){
    return x,y
    return y,x
}
```

同个 类型 可以不用标注出参数
并且，支持多个同时返回.

命名返回参数(named return values)

```go
package main

import "fmt"

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(split(17))
}
```

## varibale

```go
var i int,b float,

//  作为一个现代语言，类型推断显然是有的
var x = 132

// 在函数内部更是
// 不需要var 来declare.

x := 123

// 作为现代语言 适当的初始化显然是有的

// 默认初始化为 0 for integer string 为 "" false 为 bool 
```

### ALL TYPES

bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128

### Contant

```
const sth = sth
```

const 没有类型？取而代之 根据上下文确定类型：

```go

package main

import "fmt"

const (
	// Create a huge number by shifting a 1 bit left 100 places.
	// In other words, the binary number that is 1 followed by 100 zeroes.
	Big = 1 << 100
	// Shift it right again 99 places, so we end up with 1<<1, or 2.
	Small = Big >> 99
)

func needInt(x int) int { return x*10 + 1 }
func needFloat(x float64) float64 {
	return x * 0.1
}

func main() {
	fmt.Println(needInt(Small))
	fmt.Println(needFloat(Small))
	fmt.Println(needFloat(Big))
	fmt.Println(needInt(Big))
	
}
```

needInt 报错


## for loop

```go
for i:=0;i<10;i++{
    fmt.Println(i)
}

another form:
for i<1000 {
    fmt.println()
}
another:

for ;condition; {

}

infinite loop:
for {

}

```

注意一个特点 condition 没有 brace. 事实上
if 也没

## if

```go

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}

```

if 还支持这种局部命名方式。

## switch 

switch 语句重要不同
switch case不需要是常量 。 不需要加break. 自动break

```go


package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("macOS.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}
```

## switch with long condition

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}
```
用来写 多种情况的if-else

## defer 语句

[https://go.dev/blog/defer-panic-and-recover]
推迟  函数调用。知道周围函数推出之后彩绘执行。
Defer is commonly used to simplify functions that perform various clean-up actions.
遵循栈的顺序进行调用
some rules:
- A deferred function’s arguments are evaluated when the defer statement is evaluated.
- stack based.
-
## go 的指针

go 指针没有算术运算

## go的结构体

```go
type Vertex struct{
    x int 
    Y int 
}


func main() {
	v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
}
// we allonw direct use of pointer for structer (no -> needed)

like this:
var pointer *Vertex = &v
pointer.x
pointer.y
```

## go的array

go的array是 这样的

```go
var arrary [10]int
```

注意 array不可变也就是说 array类型本省的长度是一部分

## slice

好了 那么 slice就是我们这里的重头戏了。
slice是可变列表与array区别是[]之中没有了数字。
注释：**[...]int也是array自动推导的array**
遵循左臂有开。

slice 有 类似python slice的特性。他是引用原先元素的。

### length与 capativey

len() =>length
cap() => capactivy

容量就是底层数组。

注意，s=s[2:9] 这样取出元素会影响cap 而 s=s[:3]往前缩小，不会影响cap,并且之后扩张回原样会发现是一样的。

### make创建

```go
a_dynamic_array=make([]int,0,5)
```

type,length,cap

## for range

```go
package main

import "fmt"

var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```

i 是 index,v就是value。likepython,use a _ to omit value .

## map 用法

```go
package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

var m map[string]Vertex

func main() {
	m = make(map[string]Vertex)
	m["Bell Labs"] = Vertex{
		40.68433, -74.39967,
	}
	fmt.Println(m["Bell Labs"])
}

```

### 删除map元素

```go
delete(m,key)
```

### key in map

```go
elem, ok := m[key]
```

## type method(class)

A method is a function with a special receiver argument.
方法是具有特殊接收器参数的函数。

有意思，方法是单独定义的么。go 没有类

看起来像是一种语法糖 因为 Abs(v) 和 v.Abs()貌似是同一种效果。 不过python也是。

#### 非struct 也可以定义这样的方法

```go
//这个语句是一个类型生命类似的东西
type myFloat float64

func (v myFloat) testFunc(){
    return v
}

```


#### 同一个包的才能进行定义操作

#### type receiver 可以是指针

根据前面语法🍬的理解，这里不难解释，如果想要修改类的属性，那么必须使用指针作为参数了。

并且 Go 会将 v.PointerArgument() => PointerArgument(&v) 自动转换。

## interface  

同 Typescript. 实现接口 不需要implement等等关键词  
只要方法到位就可

### interface 里是nil 和 interface 本省是nil的区别

```go
type A interface{
    M()
}
var variable_a sth_implA
a = nil
那么
var sth A  就是一个nil interface
而  var sth A = varibale_a 那么 sth 就不是nil 因为 有了类型。


```

### 类型推断

从 interface 中拿出具体直

```go

package main

import "fmt"

func main() {
	var i interface{} = "hello"

	s := i.(string)
	fmt.Println(s)

	s, ok := i.(string)
	fmt.Println(s, ok)

	f, ok := i.(float64)
	fmt.Println(f, ok)

	f = i.(float64) // panic
	fmt.Println(f)
}
如果没有有ok 那么当尝试取出不存在的志，就会出发panic
```

#### 类型断言族的switch 

```go


package main

import "fmt"

func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)
	do("hello")
	do(true)
}
```

### fmt.println的背后

所有类型 寻找 Stinger 接口，也就是String()函数，返回string

```go

type stringer interface{
    String() string
}

这是错误的处理方式 所有的错误类型需要实现 Error()接口
i, err := strconv.Atoi("42")
if err != nil {
    fmt.Printf("couldn't convert number: %v\n", err)
    return
}
fmt.Println("Converted integer:", i)
```
### type 不同于ts的仅仅只是一个类生命，他是一种全新类型，但是标注了底层类型。

### Read方法 与 io 相关的都会提供

```go

func (T) Read (to_populate byte[]) (bytes_read int,is_error err)
```

## Image Interface 

```go
package image

type Image interface {
    ColorModel() color.Model
    Bounds() Rectangle
    At(x, y int) color.Color
}

```

## Type Generics 类型

```go
package main

import "fmt"

// Index returns the index of x in s, or -1 if not found.
func Index[T comparable](s []T, x T) int {
	for i, v := range s {
		// v and x are type T, which has the comparable
		// constraint, so we can use == here.
		if v == x {
			return i
		}
	}
	return -1
}

func main() {
	// Index works on a slice of ints
	si := []int{10, 20, 15, -10}
	fmt.Println(Index(si, 15))

	// Index also works on a slice of strings
	ss := []string{"foo", "bar", "baz"}
	fmt.Println(Index(ss, "hello"))
}

```

## go coroutines:

只需要
```go

go afunc()

```

就能出发

### Channel 用于 go coroutines 的同步 类似管道

```go
package main

import "fmt"

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum // send sum to c
}

func main() {
	s := []int{7, 2, 8, -9, 4, 0}

	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)
	x, y := <-c, <-c // receive from c

	fmt.Println(x, y, x+y)
}
```

chan must bed made before being used.

#### channels 是 bufferd

如果channel满了，就会堵塞在那里。

#### 关闭channel 与检测是否关闭

```go
v, ok := <-ch
The loop for i := range c receives values from the channel repeatedly until it is closed.
close(ch)
```

channel的关闭始终由发送者进行，否则会造成panic。

关闭不是必须的。只有像for loop 才需要。

#### select 语句

```go
func fibonacci(c, quit chan int) {
	x, y := 0, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}
```
哪个可以运行就哪个，如果好几个，那就随机一个。

#### safe guard: mutex

```go

package main

import (
	"fmt"
	"sync"
	"time"
)

// SafeCounter is safe to use concurrently.
type SafeCounter struct {
	mu sync.Mutex
	v  map[string]int
}

// Inc increments the counter for the given key.
func (c *SafeCounter) Inc(key string) {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
	c.v[key]++
	c.mu.Unlock()
}

// Value returns the current value of the counter for the given key.
func (c *SafeCounter) Value(key string) int {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
    // 这个defer 很有C++ guard 的味道
	defer c.mu.Unlock()
	return c.v[key]
}

func main() {
	c := SafeCounter{v: make(map[string]int)}
	for i := 0; i < 1000; i++ {
		go c.Inc("somekey")
	}

	time.Sleep(time.Second)
	fmt.Println(c.Value("somekey"))
}
```

## 包级别 只允许生命变量，而且不能后续进行赋值，除非初始化赋值。

## 更多go 的学习资料

[https://go.dev/tour/concurrency/11]
You can get started by installing Go.

Once you have Go installed, the Go Documentation is a great place to continue. It contains references, tutorials, videos, and more.

To learn how to organize and work with Go code, read How to Write Go Code.

If you need help with the standard library, see the package reference. For help with the language itself, you might be surprised to find the Language Spec is quite readable.

To further explore Go's concurrency model, watch Go Concurrency Patterns (slides) and Advanced Go Concurrency Patterns (slides) and read the Share Memory by Communicating codewalk.

To get started writing web applications, watch A simple programming environment (slides) and read the Writing Web Applications tutorial.

The First Class Functions in Go codewalk gives an interesting perspective on Go's function types.

The Go Blog has a large archive of informative Go articles.

Visit the Go home page for more.
