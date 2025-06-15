# soft link
ln -s 相对于 链接所在目录，如果是相对链接
# 硬链接和软连接。
。。。这个在unix那本书里有讲，太早了，都忘了。
硬链接是一个指向文件（inode?）的指针。
软连接是个指向硬链接的链接。 
# shell通配符:
*若干个字符
?一个字符
[(!可加 表示反转)]一组字符中的单个
# 重定向
2>&1表示将2和1合二为一  
注释：2>1 1不是stdin,而回创建一个单独的文件
# tee 命令
管道中的T ，保存stdin到文件并且发送出去到下一个
# process substition
执行形如 
>(rev)的命令，会使得shell创建一个临时文件作为pipe,这个pipe 传送数据到里面的rev命令。
实际命令中 rev被替换成对应的shell。  
echo >(rev)既可以看到这个管道的具体路径。
可以把他看成是一个子进程
## pactice:
```
hacker@piping~split-piping-stderr-and-stdout:~$ /challenge/hack 2>(/challenge/the) 1>(/challenge/planet)
It looks like you passed something like '>(something)' as an *argument* to 
/challenge/hack rather than redirecting /challenge/hack's out/error to 
'>(something)'. Remember, 'cmd1 >(cmd2)' does *NOT* redirect output of cmd1; 
rather, it'll run cmd2, hook a file up to its standard input, and pass that 
file as an argument to cmd1. If you want to redirect cmd1's output into that 
file, you will need to do: 'cmd1 > >(cmd2)', which is equivalent to 'cmd1 | 
cmd2'.
You must redirect my standard output into '/challenge/planet'!
You must redirect my standard error into '/challenge/the'!
Are you sure you're properly redirecting /challenge/hack's standard output into 
'/challenge/planet'?
Are you sure you're properly redirecting /challenge/hack's standard error into 
'/challenge/the'?
hacker@piping~split-piping-stderr-and-stdout:~$ /challenge/hack 2> >(/challenge/the) 1> >(/challenge/planet)
Congratulations, you have learned a redirection technique that even experts 
struggle with! Here is your flag:
pwn.college{YjcVxlRTEGviumMBGm5vrd_L8Qq.QXxQDM2wiM2cjMyEzW}

```
remeber that >(sth) is a file !
# 变量：
$用于访问，而 直接复制不需要$,注意不要多空格，否则当成是程序。
# quote:
quote用于连接带空格的变量
# 导出变量：

 sth=123
sth会暴露给子进程
# env 查看所有变量
# 读取用户输入 read 
read < 可以读取文件
# ps
默认输出当前shell中执行的
ps -ef ps aux更为常用
加上ww禁止截断  
awk for complex text processing
cut for extracting parts of lines
less for an interactive file reader
more to read parts of files at a time
paste to combine files
sed for complex text manipulation
sort for sorting data
tail as an inverse of head
uniq for filtering out unique data in a stream
# ctrl+z 睡眠，挂起终端,命令fg用于恢复
   - `S`: 挂起（也称为阻塞）
   - `R`: 运行中
   - `T`: 正在运行，但没有输出缓冲区
   - `W`: 尝试中断或暂停进程
   - `X`: 错误或未定义的状态
# 错误代码
echo $?
# chown change owner
# id 查看组别  以及信息
# chmod:
首字符
user|group|other +|- rwx
# ch子辈所需权限：
```markdown
这三个命令（`chmod`、`chown`、`chgrp`）都用于改变文件的权限或归属，但**它们对执行者的权限有不同要求**。下面是详细对比：

---

## ✅ 1. `chmod`（修改权限）

- **作用**：修改文件或目录的读/写/执行权限。
- **执行者要求**：
  - 必须是该**文件的拥有者**，或者
  - 是 **root**

✅ **普通用户只能修改自己拥有的文件的权限**。

### 示例：
```bash
chmod 755 myfile.txt   # 前提是你是 myfile.txt 的所有者
```

---

## ✅ 2. `chown`（修改文件所有者和所属组）

- **作用**：更改文件的用户和/或组的归属。
- **执行者要求**：
  - **只有 root 用户** 可以修改文件的所有者（UID）！

❌ **普通用户不能使用 `chown` 来把文件归属改成别人，即使你是文件的拥有者。**

### 示例：
```bash
sudo chown user1 file.txt       # 改变所有者
sudo chown user1:group1 file.txt # 同时改变所有者和组
```

---

## ✅ 3. `chgrp`（修改所属组）

- **作用**：只更改文件所属的组（GID）。
- **执行者要求**：
  - 是**文件的拥有者**
  - 并且你要设置的**目标组是你所属的组之一**
  - 或者是 **root**

✅ **普通用户可以把自己文件的组改成自己所属的其他组**。

### 示例：
```bash
chgrp devgroup file.txt  # 如果你是 file.txt 的拥有者，且 devgroup 是你所在的组之一
```

---

## ✅ 总结对比表：

| 命令    | 功能                 | 谁能执行                         |
|---------|----------------------|----------------------------------|
| `chmod` | 改权限（rwx）         | 文件拥有者 或 root               |
| `chown` | 改用户和/或组         | **仅限 root**                    |
| `chgrp` | 改组                  | 文件拥有者（组必须属于自己） 或 root |

---

## 🧠 例外提示：

- **即使你是超级用户（root），也要小心使用 `chown -R` 和 `chmod -R`，因为可能会破坏系统权限结构。**
- 文件系统如 `NTFS`、`FAT32`（如 USB）在挂载时权限可能会失效，尤其是在 Linux 中。

---

如果你想具体分析某个文件是否可以被谁改权限或归属，贴出 `ls -l` 和当前用户信息我可以帮你判断。

# cat /etc/passwd
这个文件存了一些用户信息，原本是村密码的，但现在已经不用了。(现在使用etc/shadow，并非安全，开膛手杰克软件可以破解)
# su
原理是设置 setuid位(chmod u+s)
# sudo
更为安全，不是简单的查看密码（su does）,有一些检查策略
sudors文件操控权限
check this:https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file#how-to-give-a-user-sudo-privileges
# .bashrc
like .zshrc ，是启动脚本，启动自定义执行（警告 .bashrc可能是全局刻度的（还真是，我在自己的wsl是试了一下）,不要存放铭感数据）
还有一些文件（.bash_logout退出使用，.bash_histroy，存储历史记录
# 对于目录的执行权限
代表能进入
# 对于目录的读权限，不必多说，对于目录的写权限
代表能在里面创建删除文件
- **读权限**：这表示用户可以读取目录中的所有文件或目录。
- **写权限**：这表示用户可以添加、删除和修改目录中的文件或目录。
- **执行权限**：这表示用户可以运行目录中的程序。
这导致了一个很有趣的事情，如果有一个全局可写的目录，那么其他用户可以删掉里面的文件在弄一个同名字的。
# /tmp 目录的特殊之处
粘滞位（t）也就是防止我们上面的那些技巧 即使tmp权限大开也无法进行文件篡改
The sticky bit means that the directory only allows the owners of files to rename or remove files in the directory. 
# 在命令行中args带密码是不安全的 ps aux可以qie🐧取到

# the fork bomb:
不断重复启动进程直到卡死
# yes!
通过不断输出yes填满内存
# rm -rf/ 仍然可以用shell 完就一切



./ ok now i finish all cousrse!