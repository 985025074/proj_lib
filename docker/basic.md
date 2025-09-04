# docker 学习记录

## docker 安装

```sh
sudo pacman -S docker
```

然后启动服务

```sh
sudo systemctl start docker.socket
```

这里使用 docker.socket是为了不要开机启动，提升boot 速度。  
docker 默认需要root权限才可以工作,你可以添加到组docker。  

## docker 的运行 基本机理

当读者安装Docker的时候，会涉及两个主要组件：Docker客户端和
Docker daemon（有时也被称为“服务端”或者“引擎”）。
daemon实现了Docker引擎的API。
使用Linux默认安装时，客户端与daemon之间的通信是通过本地
IPC/UNIX Socket完成的（/var/run/docker.sock ）；在Windows上是通
过名为npipe:////./pipe/docker_engine 的管道（pipe）完成的。读
者可以使用docker version 命令来检测客户端和服务端是否都已经成功运
行，并且可以互相通信。

## docker 基础命令

```sh
sudo docker image ls

sudo docker image pull ..

# 启动docker 容器 并且进入交互式终端shell 
sudo docker container run -it

sudo docker ---- ls 注意可以加上-a 等 不然只会列出正在运行的docker 容器 

# 连接已经运行的docker容器：
# 推出方法：ctrl + PQ
sudo docker container exec -it [nameer or id] [command like bash] 

# 停止 + 删除
stop  remove 
```

## 原理

dameon -> containred -> shrim 接管 runc推出之后的工作。
具体容器工作由内部人员进行。

## 镜像拉取

latest 并非最新 有的是edge


