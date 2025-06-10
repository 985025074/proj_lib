# 32寄存器自带余下清零，而其余的不带
eax 32位 rax 64位
# mov方向 右到左
# movsx 32->64 低到高用 + 符号拓展
# rip next insturction
# rsp 栈顶寄存器

# syscall

mov sth,num  
syscall

# exit是60
rdi传递退出代码
# 手动生成可执行过程：
```asm
.intel_syntax noprefix
要加上这一行

```
as ld
## 添加_start
global _start:


_start:

# strace查看系统调用

# 一个地址一个字节
地址计算
[base+index*[248]+ sth]
栈 位于虚拟内存
# 大部分都是小端序[]存入内存地址

# 根据gpt:
rsp可以操作，通过一些指令
而rip 只可以【rip】访问对应内容，而无法操作riip本身

# 写到内存
如果是从寄存器写，那一切好说，但是如果是写入立即数，那么必须指定大小
mov DWORD PTR like this <-
# 系统调用 与 函数C 的关系：
read ()
翻译成 
mov
mov
mov
mov
syscall
# write 调用 号 为 1
参数通过rdi,rsi，rdx,r10,r8,r9

# read 调用号0

# jmp 
# condition jump : ja
依据的是flag
来自于大多数的比较运算：
如 cmp test,算数运算

# 函数调用
call ret 涉及一个 push rip 和 pop rip的操作
anything to know about x86 :
https://www.felixcloutier.com/x86/
mov ax,0x1337
mov r12,0xCAFED00D1337BEEF
mov esp,0x31337
# mov rax,0 mov eax,0都能将整个请0，然而对于ax 则不行

# mov 低位字节可以直接实现特定位数的取模