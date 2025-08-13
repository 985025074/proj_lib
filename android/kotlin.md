# 实例：
```kotlin
fun name(){

}
```
按照驼峰
类似 Js 没有分号
# print: println
# 变量类型：
String Int Double Float Boolean

# 变量声明：
```
val count: Int = 2
```
like 
let sth : type = number

支持类型推断
# 字符串模板
```js

let a = `你好 ${123}`
```
```kotlin
val a:String = "你好 ${val}"
```
# 赋值操作：
支持 What you think


# 函数
# 支持返回类型标注
# 支持默认实参
貌似没有 python那种先后的需要
# 空返回值 Unit ： void

# 参数类似与 Python 是传的“标签”：

不同之处是：
```kotlin
/**
 * You can edit, run, and share this code.
 * play.kotlinlang.org
 */
fun helloworld(number:Int){
    number ++
    return number
}
fun main() {
    val sth = 123
    helloworld(sth)
    println("$sth + sth ")
}

```
不同之处是kotlin 会直接报错。（var 不会，但仍然是拷贝纸 ）
# 调用的时候支持传递名
println(birthdayGreeting(name = "Rex", age = 2))
顺序随意

