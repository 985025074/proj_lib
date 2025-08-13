# 分区：
1. lsblk: 查看磁盘情况：
```
yicong@yicong-VMware-Virtual-Platform:~/桌面$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
fd0      2:0    1  1.4M  0 disk 
loop0    7:0    0    4K  1 loop /snap/bare/5
loop1    7:1    0 73.9M  1 loop /snap/core22/1748
loop2    7:2    0  258M  1 loop /snap/firefox/5751
loop3    7:3    0 11.1M  1 loop /snap/firmware-updater/167
loop4    7:4    0 91.7M  1 loop /snap/gtk-common-themes/1535
loop5    7:5    0  516M  1 loop /snap/gnome-42-2204/202
loop6    7:6    0 10.8M  1 loop /snap/snap-store/1248
loop7    7:7    0 44.4M  1 loop /snap/snapd/23545
loop8    7:8    0  568K  1 loop /snap/snapd-desktop-integration/253
loop9    7:9    0  576K  1 loop /snap/snapd-desktop-integration/315
sda      8:0    0   50G  0 disk 
├─sda1   8:1    0  1.9G  0 part [SWAP]
├─sda2   8:2    0    1M  0 part 
└─sda3   8:3    0 48.1G  0 part /
sr0     11:0    1 89.4M  0 rom  /media/yicong/CDROM
sr1     11:1    1  5.9G  0 rom  /media/yicong/Ubuntu 24.04.2 LTS amd64


```
loop设备：根据gpt解释：

把一个文件 当成一个设备（磁盘）
此处我们的sda 已经满了。
设置VM 虚拟磁盘解决.
# 扩展之后再次 lsblk
注意不是扩容磁盘！！
# sudo fdisk 
按G 使用 gpt分区
分区号 (1,2, 默认  2): 1

         Device: /dev/sdb1
          Start: 2048
            End: 4196351
        Sectors: 4194304
           Size: 2G
           Type: Linux swap
      Type-UUID: 0657FD6D-A4AB-43C4-84E5-0933C84B4F4F
           UUID: DEFD3156-C8D9-461E-9F46-5B5D0322E25A

命令(输入 m 获取帮助)： i
分区号 (1,2, 默认  2): 2

         Device: /dev/sdb2
          Start: 4196352
            End: 52426751
        Sectors: 48230400
           Size: 23G
           Type: Linux 文件系统
      Type-UUID: 0FC63DAF-8483-4772-8E79-3D69D8477DE4
           UUID: 012EA71B-A196-467F-9E44-592F1366D891

注： 分区完毕之后 fdisk 并未显示swap.不知什么原因

# 格式化 文件系统：
mkfs -v -t ext4 /dev/<xxx>
选项意义：verbose + ext4

mkswap /dev/<yyy>
交换分区初始化

# 挂载分区以进行操作：export LFS=/mnt/lfs
为了方便 写入bashrc
# 设置文件模式编码：
umask 022 。移除其他人的写权限
注意确保umask 022 + LFS  环境变量正确
# 挂载：
mkdir -pv $LFS
mount -v -t ext4 /dev/sdb $LFS

# 自动挂载：防止重启后丢失：
/dev/sdb2  /mnt/lfs ext4   defaults      1     1

# swap 分区启用
/sbin/swapon -v /dev/sdb1

# 软件包：

sudo mkdir -v $LFS/sources
将此目录设置为可写且粘性。 “ 粘性 ” 意味着即使 多个用户对目录具有写权限，只有所有者 可以删除粘性目录中的文件。 以下命令将启用写入和粘性模式：

wget --input-file=wget-list-sysv --continue --directory-prefix=$LFS/sources
按照地址下载 + 断电重传 + 指定保存地址
# md5 检查
pushd $LFS/sources
  md5sum -c md5sums
popd
# 更改这些用户所有者：
防止在LFS  中 显示是Unknown

# 下载完包之后；
```sh
mkdir -pv $LFS/{etc,var} $LFS/usr/{bin,lib,sbin}

for i in bin lib sbin; do
  ln -sv usr/$i $LFS/$i
done

case $(uname -m) in
  x86_64) mkdir -pv $LFS/lib64 ;;
esac

```
tools 目录create

#  LFS 用户创建：
```
groupadd lfs
useradd -s /bin/bash -g lfs -m -k /dev/null lfs

```
-k 防止有默认配置
# 改变文件权限。
参考文档
# 警告！sudo 之后环境变量不见！
# 干净的用户shell配置：
```sh
cat > ~/.bash_profile << "EOF"
exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
EOF
```
 shell 实例是非登录 shell，它不会读取和执行 /etc/profile 或 .bash_profile 文件的内容，而是读取和执行 .bashrc 文件。现在创建 .bashrc 文

# 进一步完善
脚本的解释：https://www.linuxfromscratch.org/lfs/view/stable/chapter04/settingenvironment.html
```sh
cat > ~/.bashrc << "EOF"
set +h
umask 022
LFS=/mnt/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu
PATH=/usr/bin
if [ ! -L /bin ]; then PATH=/bin:$PATH; fi
PATH=$LFS/tools/bin:$PATH
CONFIG_SITE=$LFS/usr/share/config.site
export LFS LC_ALL LFS_TGT PATH CONFIG_SITE
EOF
```
一些商业发行版在 bash 的初始化过程中添加了一个未记录的 /etc/bash.bashrc 实例。该文件可能会修改 lfs 用户的环境，从而影响关键 LFS 软件包的构建。为了确保 lfs 用户的环境干净，请检查 /etc/bash.bashrc 是否存在，如果存在，请将其移除。以 root 用户身份运行：

[ ! -e /etc/bash.bashrc ] || mv -v /etc/bash.bashrc /etc/bash.bashrc.NOUSE

# 设置多核运行：
使用nrpoc 检查核心 虚拟机是4
cat >> ~/.bashrc << "EOF"
export MAKEFLAGS=-j$(nproc)
EOF
# 软件构建：
```
Here is a synopsis of the build process.
以下是构建过程的概要。

Place all the sources and patches in a directory that will be accessible from the chroot environment, such as /mnt/lfs/sources/.
将所有源和补丁放在一个目录中 可以从 chroot 环境访问，例如 /mnt/lfs/sources/ 。

Change to the /mnt/lfs/sources/ directory.
切换到 /mnt/lfs/sources/ 目录。

For each package:   对于每个包：

Using the tar program, extract the package to be built. In Chapter 5 and Chapter 6, ensure you are the lfs user when extracting the package.
使用 tar 程序解压要构建的包。在第 5 章和第 6 章中，请确保您是 lfs 用户 提取包时。

Do not use any method except the tar command to extract the source code. Notably, using the cp -R command to copy the source code tree somewhere else can destroy timestamps in the source tree, and cause the build to fail.
不要使用除 tar 命令之外的任何方法来 提取源代码。值得注意的是，使用 cp -R 命令复制源 其他地方的代码树可能会破坏时间戳 在源树中，并导致构建失败。

Change to the directory created when the package was extracted.
更改为提取包时创建的目录。

Follow the instructions for building the package.
按照说明构建包。

Change back to the sources directory when the build is complete.
构建完成后，返回源目录。

Delete the extracted source directory unless instructed otherwise.
除非另有指示，否则删除提取的源目录。

```

# 时间测量：
 time { ../configure ... && make && make install; } 。
# 构建过程解释：
第一遍构建出的工具是：
LFS 第一遍构建出的工具，确实是临时工具链，用来为后续构建整个 LFS 系统提供基础编译和链接工具。
binutils (第一遍)

包含汇编器 as 和链接器 ld，负责把汇编代码变成机器码和链接目标文件。

必须先编译安装，因为后面编译 gcc 和 glibc 都依赖汇编和链接工具。

gcc (第一遍)

编译一个只包含 C 编译器的最小版 gcc，供后续编译 glibc 使用。

配置时指定临时工具链里的 binutils，确保用的是刚刚构建的汇编器和链接器。

Linux API 头文件

提供内核接口定义，保证 glibc 能正确调用内核功能。

glibc

标准 C 库，所有 Linux 程序依赖它。（printf 的实现）

用刚才编译好的临时 gcc 和 binutils 编译。

libstdc++

GCC 的标准 C++ 库，部分后续程序可能用到。

其他必须的交叉编译程序

用来解决构建过程中循环依赖问题。
# binutils:
连接器  + 汇编器 
1. lfs:/mnt/lfs/sources$ tar -xf binutils-2.44.tar.xz 

mkdir -v build
cd       build
 2. 
 ```sh
 time{
   ../configure --prefix=$LFS/tools \
             --with-sysroot=$LFS \
             --target=$LFS_TGT   \
             --disable-nls       \
             --enable-gprofng=no \
             --disable-werror    \
             --enable-new-dtags  \
             --enable-default-hash-style=gnu
  && make && make install 
 }
 ```
 注意严格空格 上述只是示例
 real	1m7.197s
user	2m23.266s
sys	1m3.737s


# 安装完一些列包之后：
操作 文件为root (新系统的root)
# 完成其他一些工作(系统所需的其他文件夹)：
添加/dev。
这里暂时挂载原有的dev (bind)
mount -v --bind /dev $LFS/dev
mount -vt devpts devpts -o gid=5,mode=0620 $LFS/dev/pts
mount -vt proc proc $LFS/proc
mount -vt sysfs sysfs $LFS/sys
mount -vt tmpfs tmpfs $LFS/run

# 进入LFS 系统工作！
此时 我们将不在使用/tools 而是使用/bin 的工具了（前者创建）
```sh
chroot "$LFS" /usr/bin/env -i   \
    HOME=/root                  \
    TERM="$TERM"                \
    PS1='(lfs chroot) \u:\w\$ ' \
    PATH=/usr/bin:/usr/sbin     \
    MAKEFLAGS="-j$(nproc)"      \
    TESTSUITEFLAGS="-j$(nproc)" \
    /bin/bash --login
```
# 注意
FHS 并不强制要求目录的存在 /usr/lib64 和 LFS 编辑器 决定不使用它。有关 LFS 和 BLFS 中的说明 为了正常工作，必须将此目录设置为 不存在。你应该时不时地验证它是否 不存在，因为很容易在无意中创建它，并且 这可能会破坏你的系统。
# 创建proc:
proc 是 Linux 下的一个特殊的虚拟文件系统，挂载在 /proc 目录下。

它不是普通的磁盘文件系统，而是由内核实时生成的，用来向用户空间暴露内核和系统运行时的各种信息。
# 创建用户密码：etc/passwd 和用户组：
掠过

# 日志系统：
```
touch /var/log/{btmp,lastlog,faillog,wtmp}
chgrp -v utmp /var/log/lastlog
chmod -v 664  /var/log/lastlog
chmod -v 600  /var/log/btmp

```