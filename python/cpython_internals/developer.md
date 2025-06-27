# 关于Cpython 项目配置
首先查看cpython 官网的dev guide.  
首先安装pre-commit.pre-commit 安装:`sudo apt install pre-commit`.
然后在get_started 这一个page现状dependencies.  
注意ubuntu24有一些包是无法安装的。
# 项目运行：
首先configure:
`./configure --with-pydebug`

`make -s -j $(nproc)`

# 实战：修改python 语法：
https://github.com/python/cpython/blob/main/InternalDocs/changing_grammar.md
先来个简单的试试水：
修改lambda语法，成js格式。
```js
func = ()=>{}
```
简单的修改gram会导致原先的一些代码崩溃。因此我们打算完全添加一个新的语法。
查看原先lambda 的定义：
```
lambdef[expr_ty]:
    | 'lambda' a=[lambda_params] ':' b=expression {
        _PyAST_Lambda((a) ? a : CHECK(arguments_ty, _PyPegen_empty_arguments(p)), b, EXTRA) }


```
这里的语法意思是lambda def是规则名。右边的匹配样式，而左边的则是产生对应的AST 方法。
查询上门的markdown，进到对应的AST
**python .asdl** 文件是定义AST节点的文件。
我们在里面加入我们的AST 节点
```
         | SetComp(expr elt, comprehension* generators)
         | DictComp(expr key, expr value, comprehension* generators)
         | GeneratorExp(expr elt, comprehension* generators)
         -- SYC made 
         | MyLambda(arguments args, expr body)
         -- the grammar constrains where yield expressions can occur
         | Await(expr value)
         | Yield(expr? value)
         | YieldFrom(expr value)
```
OK 加入我们的lamda.
然后需要改一下parser规则，以便产生对应的ast 节点.
也就是python.gram。
ctrl + f 添加上所有的定义。跟在lambdadef后即可。
然后 加上myLambda 定义。
这里用的就是单个token，我不确定行不行，可能触发某些语法错误。
先试试，如果不行，后面再改成'=>'这样的token
```
# ----------------
myLambda[expr_ty]:
    | '(' a=[lambda_params] ')''=''>' b=expression {
        _PyAST_MyLambda((a) ? a : CHECK(arguments_ty, _PyPegen_empty_arguments(p)), b, EXTRA) }

lambdef[expr_ty]:
    | 'lambda' a=[lambda_params] ':' b=expression {
        _PyAST_Lambda((a) ? a : CHECK(arguments_ty, _PyPegen_empty_arguments(p)), b, EXTRA) }

```
执行对应make 命令，没有出错，很好.
OK。
接下来我们尝试编译整个项目。
也可以。
但是具体的代码就不行：
```
❯ ../python test.py
Traceback (most recent call last):
  File "/home/kokona/python_dev/cpython/cpython/Experiments/test.py", line 7, in <module>
    tree = ast.parse(source_code)
  File "/home/kokona/python_dev/cpython/cpython/Lib/ast.py", line 46, in parse
    return compile(source, filename, mode, flags,
                   _feature_version=feature_version, optimize=optimize)
  File "<unknown>", line 2
    func = ()=>{}
              ^
SyntaxError: invalid syntax
❯ 
```
（这里报错的原因以后有机会再研究一下！）
那我们尝试一下两个token 一起。
在python.gram同目录下的tokens中添加：
```
RARROW                  '->'
ELLIPSIS                '...'
COLONEQUAL              ':='
EXCLAMATION             '!'
RIGHTEQUAL              '=>'
```


又报错了：
```
 <module>
    tree = ast.parse(source_code)
  File "/home/kokona/python_dev/cpython/cpython/Lib/ast.py", line 46, in parse
    return compile(source, filename, mode, flags,
                   _feature_version=feature_version, optimize=optimize)
  File "<unknown>", line 2
    func = ()=>{}
             ^^
SyntaxError: invalid syntax

```
tokenize结果：
```
❯ ../python test1.py
64 (NL): 

1 (NAME): func
56 (OP): =
56 (OP): (
56 (OP): )
56 (OP): =>
56 (OP): {
56 (OP): }
4 (NEWLINE): 

0 (ENDMARKER): 

```
为什么会出错呢...
---
更新：22点48分 2025年6月22日
出错原因找到了
```
expression[expr_ty] (memo):
    | invalid_expression
    | invalid_legacy_expression

    | a=disjunction 'if' b=disjunction 'else' c=expression { _PyAST_IfExp(b, a, c, EXTRA) }
    | lambdef
    | myLambda
    | disjunction

```
disjunction 一旦放在前面就不行。
看来我要了解下parser.md...
## parser.md 阅读笔记
https://github.com/python/cpython/blob/main/InternalDocs/parser.md
- 这意味着在 PEG 语法中，选择运算符不可交换。此外，与上下文无关语法不同，根据 PEG 语法进行的推导不会产生歧义：如果一个字符串可以解析，则它只有一棵有效的解析树。
- PEG 解析器通常构建为递归下降解析器，其中语法中的每条规则都对应于实现解析器的程序中的一个函数，而解析表达式（规则的“展开”或“定义”）代表该函数中的“代码”。每个解析函数在概念上都以输入字符串作为参数。这段话的意思是，解析器生成器生成的parser 会调用asdl文件中生成的对应函数
- https://github.com/python/cpython/blob/main/InternalDocs/parser.md#key-ideas
### 选择规则是贪心的：
    first_rule:  ( 'a' | 'aa' ) 'a'
    second_rule: ('aa' | 'a'  ) 'a'
  一旦匹配到一个就一路走到头，因此两个描述是不同的

### 语法规则基本格式：
  rule_name[return_type]: expression
  更多详细规则：      [ rule_name\[return_type\]: expression](https://github.com/python/cpython/blob/main/InternalDocs/parser.md#grammar-expressions)
### 支持左递归
### 支持变量：
然后可以在动作（{}内部）使用这个var:
```
    rule_name[return_type]: '(' a=some_other_rule ')' { a }
```
### 代码动作：
就是上面说的，注意每个都要有括号，对于不同的分支。
如果没有：
If there is a single name in the rule, it gets returned.
如果规则中只有一个名称，则返回该名称。
If there are multiple names in the rule, a collection with all parsed expressions gets returned (the type of the collection will be different in C and Python).
如果规则中有多个名称，则会返回包含所有已解析表达式的集合（集合的类型在 C 和 Python 中会有所不同）。
**不允许动作内部对于AST 节点的修改**
### 实例：
```
    start[mod_ty]: a=expr_stmt* ENDMARKER { _PyAST_Module(a, NULL, p->arena) }
    expr_stmt[stmt_ty]: a=expr NEWLINE { _PyAST_Expr(a, EXTRA) }

    expr[expr_ty]:
        | l=expr '+' r=term { _PyAST_BinOp(l, Add, r, EXTRA) }
        | l=expr '-' r=term { _PyAST_BinOp(l, Sub, r, EXTRA) }
        | term

    term[expr_ty]:
        | l=term '*' r=factor { _PyAST_BinOp(l, Mult, r, EXTRA) }
        | l=term '/' r=factor { _PyAST_BinOp(l, Div, r, EXTRA) }
        | factor

    factor[expr_ty]:
        | '(' e=expr ')' { e }
        | atom

    atom[expr_ty]:
        | NAME
        | NUMBER
```
注意上面的左递归写法。
EXTRA 提供上下文信息。atom 最小单元（单个变量或者是数字）。factor 带括号的。 term 则是一个简单算式
。expr 复杂算式 
### pegen解析器

make regen-pegen.
### 元语法，不做深入，描述pegen的规则
### Some other ktes
Strings with single quotes (') (for example, 'class') denote KEYWORDS.
带有单引号 (') 的字符串（例如， 'class' ）表示关键字。

Strings with double quotes (") (for example, "match") denote SOFT KEYWORDS.
带有双引号（“）的字符串（例如 "match" ）表示软关键字。见下
Uppercase names (for example, NAME) denote tokens in the Grammar/Tokens file.
大写名称（例如， NAME ）表示 Grammar/Tokens 文件。

Rule names starting with invalid_ are used for specialized syntax errors.
以 invalid_ 开头的规则名称用于特殊的语法错误。
### tokenize
PEG (pegen generated) 是一体化的 tokenize + parser.
但是 对于pegen来说，token 是要另外处理的
make regen-token
### 记忆化，不做深入，只需知道是语法文件中的(memo):
https://github.com/python/cpython/blob/main/InternalDocs/parser.md#memoization
### 自动变量（内置变量
EXTRA ：这是一个扩展为 (_start_lineno, _start_col_offset, _end_lineno, _end_col_offset, p->arena) ，通常用于创建 AST 节点，因为几乎所有构造函数都需要提供这些属性。所有位置变量均取自当前 token 的位置信息。

p ：解析器结构。
### 软硬关键字
软关键字 如 match  在一般上下文可以被当作变量。
而hard 如 class 无法做变量

### syntax error 的罪魁祸首
syntax error 都是parser应发的

### invalid开头的规则是为了让syntax error更好看
### 内置函数，为了便利gram，带一些内置函数（类似于内置变量），你也可以定义，详细查看链接
https://github.com/python/cpython/blob/main/InternalDocs/parser.md#generating-ast-objects


### important
$ c
使用python 生成的语法解析器！
$ python parse.py file_with_source_code_to_test.py

详细调试模式(需要configure --with-debug)：
[$ python parse.py file_with_source_code_to_test.py](https://github.com/python/cpython/blob/main/InternalDocs/parser.md#verbose-mode)
python -d 


---

回到问题,disjunction:
```
disjunction[expr_ty] (memo):
    | a=conjunction b=('or' c=conjunction { c })+ { _PyAST_BoolOp(
        Or,
        CHECK(asdl_expr_seq*, _PyPegen_seq_insert_in_front(p, a, b)),
        EXTRA) }
    | conjunction


```
大概是or 一级的表达式。 conjuction的意思也不言而喻了，就是and 表达式。
从这里能看出 and 优先级更高
下面inversion 就是not 

comparison 是逻辑比较表达式
类似 a==b 这种就是comparison
Module(
    body=[
        Expr(
            value=Compare(
                left=Name(id='a', ctx=Load()),
                ops=[
                    Eq()],
                comparators=[
                    Name(id='b', ctx=Load())]))],
    type_ignores=[])

```
好吧，查到这里还是看不出什么。试试 -d 吧  
执行命令。

`./python -d  Experiments/test2.py 2> Experiments/Error.txt`


ctrl + f锁定 succeeded的表达式
补充：ast.py 里面有一部是调用compile 的，因此 如果没有字节码就会报错，不是说ast 生成完毕就没问题。

首先尝试使用tokenize 脚本

```py
from io import StringIO
import tokenize


source_code = """
 |-
"""
"""
    你好
"""
# 将字符串转换为类文件对象
stream = StringIO(source_code)

# 使用 tokenize.generate_tokens 生成标记
for token in tokenize.generate_tokens(stream.readline):
    print(f"{token.type} ({tokenize.tok_name[token.type]}): {token.string}")
```
分词结果：
```
5 (INDENT):  
56 (OP): (
56 (OP): )
56 (OP): =>
56 (OP): {
2 (NUMBER): 123
56 (OP): }
4 (NEWLINE): 

6 (DEDENT): 
0 (ENDMARKER): 
```

....放弃了，还是用python版那个吧

13点51分 2025年6月23日 
放弃了，最后我决定尝试使用negative lookaead来。
添加一些negative lookahead 之后，成功。


## compiler.md 阅读笔记


# asdl文件
关于asdl 不做深入，简单来说就是关于ast节点的定义。

# PyArene
管理所有的内存
PyArene.AddObject()
添加分配的pyObjet
qi

# 其余的没什么好说的，值得注意的的是 有一部是 AST->字节码中间 ->CFG ->最终形态字节码

# code_object.

在新版本中 ，co_code 变成了 co_code_adaptive 可以变动

记录字节码单元：co_linetable  co_positions。
字节码单元是一个字节，一个指令往往是两个字节，从而占据两个单元

# error handling:
zero cast ,意思是，SETUP_FINALLY 这种都是中间产物，
在最终的字节码中，实际上指令是被映射到对应的处理表的。


异常表 解释：
```
❯ ./python Experiments/test2.py
  3           RESUME                   0

  4           LOAD_GLOBAL              1 (print + NULL)
              LOAD_SMALL_INT         123
              CALL                     1
              POP_TOP
              LOAD_CONST               1 (None)
              RETURN_VALUE
Code length: 28
Positions: [(3, 3, 0, 0), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 10, 13), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14)]
len: 14
❯ ./python Experiments/test2.py
  3           RESUME                   0

  4           LOAD_GLOBAL              1 (print + NULL)
              LOAD_SMALL_INT         123
              CALL                     1
              POP_TOP

  5           LOAD_GLOBAL              1 (print + NULL)
              LOAD_SMALL_INT         123
              CALL                     1
              POP_TOP

  6           LOAD_GLOBAL              1 (print + NULL)
              LOAD_SMALL_INT         123
              CALL                     1
              POP_TOP
              LOAD_CONST               1 (None)
              RETURN_VALUE
Code length: 72
Positions: [(3, 3, 0, 0), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 4, 9), (4, 4, 10, 13), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (4, 4, 4, 14), (5, 5, 4, 9), (5, 5, 4, 9), (5, 5, 4, 9), (5, 5, 4, 9), (5, 5, 4, 9), (5, 5, 10, 13), (5, 5, 4, 14), (5, 5, 4, 14), (5, 5, 4, 14), (5, 5, 4, 14), (5, 5, 4, 14), (6, 6, 4, 9), (6, 6, 4, 9), (6, 6, 4, 9), (6, 6, 4, 9), (6, 6, 4, 9), (6, 6, 10, 13), (6, 6, 4, 14), (6, 6, 4, 14), (6, 6, 4, 14), (6, 6, 4, 14), (6, 6, 4, 14), (6, 6, 4, 14), (6, 6, 4, 14)]
len: 36
❯ ./python Experiments/test2.py
   3           RESUME                   0

   4           NOP

   5   L1:     LOAD_GLOBAL              1 (print + NULL)
               LOAD_SMALL_INT         123
               CALL                     1
               POP_TOP
       L2:     LOAD_CONST               2 (None)
               RETURN_VALUE

  --   L3:     PUSH_EXC_INFO

   6           POP_TOP

   7           LOAD_GLOBAL              1 (print + NULL)
               LOAD_CONST               1 (456)
               CALL                     1
               POP_TOP
       L4:     POP_EXCEPT
               LOAD_CONST               2 (None)
               RETURN_VALUE

  --   L5:     COPY                     3
               POP_EXCEPT
               RERAISE                  1
ExceptionTable:
  L1 to L2 -> L3 [0]
  L3 to L4 -> L5 [1] lasti
```
[]就是异常表的标志 lasti代表 这部分会将lasti加入栈区，方便以后操作。
原文：
Along with the location of an exception handler, each entry of the exception table also contains the stack depth of the try instruction and a boolean lasti value, which indicates whether the instruction offset of the raising instruction should be pushed to the stack.
除了异常处理程序的位置之外，异常表的每个条目还包含 try 指令的堆栈深度和布尔值 lasti ，该值指示是否应将提升指令的指令偏移量推送到堆栈。

# frame：
frame被分配到每个线程的栈上，除开生成器 和 携程

# 垃圾回收
sys.getrefcont（x）
### 为了解决循环引用，在Pyobject ptr的前端还有一些之





# python 执行流程探究：
Program/python.c 是入口
Modules/main.c
第一个重要的函数
status = _PyRuntime_Initialize();
进去看看
直接查看pyruntime结构体的样子
Include/internal/pycore_runtime_structs.h。
## runtime中的重要字段：
```
    线程
    PyThreadState *_finalizing;
    /* The ID of the OS thread in which we are finalizing. */
    unsigned long _finalizing_id;
    有多个解释器：

   struct pyinterpreters {
        PyMutex mutex;
        /* The linked list of interpreters, newest first. */
        PyInterpreterState *head;
        /* The runtime's initial interpreter, which has a special role
           in the operation of the runtime.  It is also often the only
           interpreter. */
        PyInterpreterState *main;
        /* next_id is an auto-numbered sequence of small
           integers.  It gets initialized in _PyInterpreterState_Enable(),
           which is called in Py_Initialize(), and used in
           PyInterpreterState_New().  A negative interpreter ID
           indicates an error occurred.  The main interpreter will
           always have an ID of 0.  Overflow results in a RuntimeError.
           If that becomes a problem later then we can adjust, e.g. by
           using a Python int. */
        int64_t next_id;
    } interpreters

```
下面就不说了，是一些其他变状态量的初始化。

值得一提的是 gil_state也在这里，具体应用不清楚。

还有一个全局锁
```
    // The rwmutex is used to prevent overlapping global and per-interpreter
    // stop-the-world events. Global stop-the-world events lock the mutex
    // exclusively (as a "writer"), while per-interpreter stop-the-world events
    // lock it non-exclusively (as "readers").
    _PyRWMutex stoptheworld_mutex;
    struct _stoptheworld_state stoptheworld;
```
这个不清楚有什么用

---
回到初始化函数：
Python/pylifecycle.c _Pyruntime_initialize

再回到 Pymain_init()
下面做了两次初始化 preconfig 和 普通 config
config里是一些基本配置。
然后是从args 进行设置

args 被设置到Pyconfig上
然后从PyConfig 再次初始化runtime



