# tutorial 学习记录

## 文档结构

go.mod - 用go mod init生成 规定整个~~工程~~ 入口点的名字
go.sum - 教研和之类的玩意？

### 区别package 和 main 

这个错误的原因是：你尝试导入的 example/hello 是一个可执行程序（包含 main 包和 main 函数），而不是一个可导入的库包（通常是非 main 包）。

Go 语言规定：只有非 main 包的代码才能被其他包导入，main 包是程序入口，只能编译为可执行文件，不能被导入。


## go test

以 _test.go结尾表示是测试文件

Ending a file's name with _test.go tells the go test command that this file contains test functions.

```go
import (
    "testing"
    "regexp"
)

// TestHelloName calls greetings.Hello with a name, checking
// for a valid return value.
func TestHelloName(t *testing.T) {
    name := "Gladys"
    want := regexp.MustCompile(`\b`+name+`\b`)
    msg, err := Hello("Gladys")
    if !want.MatchString(msg) || err != nil {
        t.Errorf(`Hello("Gladys") = %q, %v, want match for %#q, nil`, msg, err, want)
    }
}

// TestHelloEmpty calls greetings.Hello with an empty string,
// checking for an error.
func TestHelloEmpty(t *testing.T) {
    msg, err := Hello("")
    if msg != "" || err == nil {
        t.Errorf(`Hello("") = %q, %v, want "", error`, msg, err)
    }
}
```

`go build / go install` 编译 + 安装 其中安装路径可以用 `go list -f '{{.Target}}'` 来找到。

## 多工作区工作实例

### go get 也可以添加依赖 跟 go mod tidy 的区别是 前者是强制添加 而后者是有选择的用到的才会添加。

后者更智能一些。

### go work 文件夹 创建 工作区

`go work init folder` 在当前目录创建一个go.work。内有工作区信息。


## 多模块 份文件注解

同个文件夹 必须同个package。
否则出错：

```go
❯ go run .
main.go:4:2: found packages a (a.go) and b (b.go) in 
/home/shiyico
```
## module内索引是 根据文件夹名的。。。 那么package 推荐 与 文件夹名一致

## GO RUN . 默认寻找当前路径下的main 包 多个文件也所谓。因为都是同个包

## 大写才能导出的规则只适用于 跨package 同 package 自由！

## package 可以重名  只要路径不同
