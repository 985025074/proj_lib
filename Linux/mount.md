# 挂载
将目录树 挂到分区
# 文件系统
带索引的：Ext 有很多权限位
连续读取：FAT
# 如：
NAME FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda  ext4   1.0                                                             
sdb  swap   1           6bf25763-722c-4683-ac79-6c34f32d8782                [SWAP]
sdc  ext4   1.0         633530b2-6495-42c4-a63c-6847928f82d0  923.7G     3% /snap
                                                                            /mnt/wslg/distro
# Ext 
整个分区是分成多个block 管理的 其中有多个x需要的数据
每个inode 可以对应多个具体数据块（间接技术，防止inode 占用过多）
# 格式化做了什么：
