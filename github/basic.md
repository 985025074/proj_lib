# github 无法识别是我提交的（commit）
方法查看github 资料中的email 选项 加入新的email地址。
# github person token作用：
可作为http 协议提交时候使用，可以使用：
```sh
使用缓存凭据助手：
设置缓存时间：执行命令git config --global credential.helper 'cache --timeout=3600'，将凭据缓存 1 小时，你可以根据需要调整timeout的值。之后在缓存时间内进行 Git 操作时，就不需要再次输入用户名和密码。
使用存储凭据助手：
永久存储凭据：执行git config --global credential.helper store命令，下次执行需要认证的 Git 操作时，Git 会提示你输入用户名和密码，输入后这些凭据将被永久存储在本地文件~/.git-credentials中。
```
来避免多次提交。
