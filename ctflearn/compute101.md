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

# mov BYTE PTR 只使用于结果是地址的情况 [addr]+ 源操作数是立即数，两个操作数不能都为间接寻址
# .rept:
重复指令：
```asm
.intel_syntax noprefix
jmp target
.rept 0x51
nop
.endr
target:
mov rax,1
```

# 跳转表：
jmp [addr]
# rbp example:
mov rbp,rsp
sub rsp,anum
...
mov rsp,rbp


# gdb usage:
basic:
run
run arg1,arg2,arg3 ....

brank *main（break *地址）

info register/brak 

del break + id

print（p $VAR 

x/(number)(foramt) instruction
x/1i
x/4gx(4 giant hex) $rsp
x/4d (4 sigend number)
x/4u unsigend number
x/4d （address
disassemble main 反汇编 main
print 也可以用格式，支持解引用 + C 风格format
display (每次si ni 都会print)

finish step out of the function

# set $VAR = sth
set设置变量。
## 可以用整个操作寄存器reg
## 为什么 break * main?:
一、为什么需要星号（*）？
默认行为：按符号名设置断点
break main：GDB 默认将 main 视为符号名（如函数名或变量名），在该符号对应的地址处设置断点。
例如：break main 会在 main() 函数的入口处暂停执行。
使用星号：指定绝对地址
break *main：* 强制 GDB 将 main 解释为内存地址（而非符号名），在该地址处设置断点。
例如：若 main 函数的地址是 0x400526，则 break *0x400526 或 break *main 都会在该地址处中断。

# gdb 脚本启动

gdb -x sth.gdb 
# 默认启动脚本呢
~/.gdbinit
set disassembly-flavour intel
read(fd,taregt,num)
# x:
您可以使用 x/<n><u><f> <address> 参数化命令检查内存内容。在此格式中， <u> 是要显示的单元大小， <f> 是显示的格式， <n> 是要显示的元素数量。有效的单元大小为 b （1 字节）、 h （2 字节）、 w （4 字节）和 g （8 字节）。有效格式为 d （十进制）、 x （十六进制）、 s （字符串）和 i （指令）。地址可以使用寄存器名称、符号名称或绝对地址来指定。此外，您还可以在指定地址时提供数学表达式
# 在指定条件停止：
start
catch syscall read
commands
  silent
  if ($rdi == 42)
    set $rdi = 0
  end
  continue
end
continue
catch

# gdb call（指定返回类型后使用

# socket系统调用
rax 41
rdi rsi，rdx参数
# bind 系统调用


<!-- 我跳过了最后一节的web环节，我觉得太折磨，也没什么意思 -->
# 数据操作
# python 进制区分：
0b 0x
# python 字节操作：

首先，字符串在python 中显示的时候都是unicode 编码（内存中），代码本身使用utf-8编码
对于一个字符串，可以进行encode（）转换成字节串（其他编码形态，python无法呈现，所以采用字节）字节，可以按照某种方式解码成python字符串
# 终端编码：
echo $LANG
大多是utf-8
对于终端无法输出的字节：
echo -e -n "\xasda"

# 文件换行符问题：
vim一个文件好像会自动添加换行符？ echo -n 是没有的


# base64:
就是6位二进制对应一个字符 =(号表示未应用的未)
例如 QQ== 十几行对应的是12 - 2*2 = 8编码
而传统的 16进制表示 是 4对应一位


# http part:
# HOST作用：
一个服务器可能跑了好几个网站，提供正确的wang'zhan

# suid只可以对user加
## 小思考：
gzip > me
为什么me 不是root？ 因为 > 是本身的行为

# suid writeup
# gccsuid bug:
# include /flag
# wc
--files0-from =/flag
直接以。flag内名称作为

# wget 解决方案：
wget --post-file=/flag
再开一个端口使用nc 接受

# cp:
使用--no-preserve 中的mode



# program interactive:
waitpid在syswait里
```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
void pwncollege(){
    
}
int main(){

    int pid = fork();

    if(pid == 0){
        execvp("/challenge/run",NULL);
        // child:
    }
    else{
        waitpid(pid,NULL,0);
    }
    return 0;
}
```

# exec:
在 C 语言中，如果 execvp() 执行成功，它后面的语句不会执行。
因为 execvp() 会直接 用新程序替换当前进程的内存空间（包括代码、堆栈、数据段等），原来的代码就被“覆盖”了。

# 进程间通信：
| 方法                 | 是否适合父子进程 | 是否适合任意进程 | 特点/说明                |
| ------------------ | -------- | -------- | -------------------- |
| `pipe`（匿名管道）       | ✅ 是      | ❌ 否      | 最简单、只能单向、父子进程间通信     |
| `named pipe`（FIFO） | ✅ 是      | ✅ 是      | 通过文件系统的路径命名，可用于无血缘关系 |
| `socket`           | ✅ 是      | ✅ 是      | 网络或本地通信，功能最强         |
| `shared memory`    | ✅ 是      | ✅ 是      | 共享一块内存区，速度最快，但需同步    |
| `message queue`    | ✅ 是      | ✅ 是      | 基于内核的消息收发队列          |
| `signal`           | ✅ 是      | ✅ 是      | 通知或控制，传数据能力弱         |
| `semaphore`（信号量）   | ✅ 是      | ✅ 是      | 不传数据，只用于同步/互斥        |

# pipe实例：
int fd[2]
pipe(fd)
完毕。0读 1写。
注意，关闭掉不用的端
# 重定向程序
dup2(src,dst)
重定向dst到src

# 好麻烦的execv arg传参：
```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
void pwncollege(){
    
}
int main(){

    int pipe_[2];
    pipe(pipe_);
    int pid = fork();

    if(pid == 0){
        // close 1 关闭写
        close(pipe_[1]);
        // redirect
        dup2(pipe_[0],0);
        // 还要带上自己
        char* const args[] = {"/challenge/run", "njgyfjlybs", 
        
        NULL};

        execv("/challenge/run",args);
        // child:
    }
    else{
        // close read
        close(pipe_[0]);
        // 
        // write(pipe_[1],"njgyfjlybs",8);
        close(pipe_[1]);

        waitpid(pid,NULL,0);
        // printf("hello!");
    }
    return 0;
}
```
# 与之相对的 C 传递 环境变量很简单，父和子一起
