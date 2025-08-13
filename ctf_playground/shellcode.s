.global _start
.intel_syntax noprefix

_start:
    # 调用 accept 获取客户端 socket fd
    lea    rax, [rbp-0x40]        # rax = sockaddr*
    mov    rcx, rax               # rcx = sockaddr*
    lea    rdx, [rbp-0x44]        # rdx = socklen_t*
    mov    eax, DWORD PTR [rbp-0x4]   # eax = 监听socket fd
    mov    rsi, rcx               # rsi = sockaddr*
    mov    edi, eax               # edi = 监听socketfd
    call   0x401340              # 调用 accept()

    mov    edi, eax               # 保存 accept 返回的 client_fd 到 edi

    # 从 client_fd 读取数据
    sub    rsp, 0x1000            # 在栈上分配 0x1000 字节作为缓冲区
    mov    rsi, rsp               # rsi = 缓冲区地址
    mov    rdx, 0x1000            # 读取最大字节数
    mov    eax, 0                 # syscall号0 = read
    syscall                       # 调用 read(client_fd, buf, 0x1000)

    # eax 中保存读取到的字节数

    # 写数据到标准输出
    mov    rdi, 1                 # fd=1 stdout
    mov    rax, 1                 # syscall号1 = write
    syscall                       # write(1, buf, eax)

    # 退出程序
    mov    eax, 60                # syscall号60 = exit
    xor    edi, edi               # 退出码0
    syscall
