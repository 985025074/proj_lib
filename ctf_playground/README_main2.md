# CIMG Python接口实现

## 概述

本文件(`main2.py`)为obj.txt反汇编文件中的所有指令提供了完整的Python接口实现。

## 反汇编分析

根据obj.txt文件，程序包含以下主要处理函数：

1. `handle_1` (0x4016d6) - 指令类型2：绘制像素数据
2. `handle_2` (0x401833) - 指令类型3：在指定位置绘制像素数据
3. `handle_3` (0x401a13) - 指令类型4：设置图层数据
4. `handle_4` (0x401c6c) - 指令类型5：复杂的图层操作和像素匹配
5. `handle_5` (0x401b3f) - 指令类型6：从文件加载数据到图层
6. `handle_6` (0x402020) - 指令类型7：显示帧缓冲区
7. `handle_7` (0x401f6b) - 指令类型8：延时指令
8. `handle_1337` (0x401e99) - 指令类型1337：特殊指令，提取图层区域数据

## 实现的Python接口

### 基础函数

- `create_cimg_header(width, height, directive_count)` - 创建CIMG文件头
- `handle_1_directive(width, height, pixel_data)` - 绘制像素数据
- `handle_2_directive(x, y, width, height, pixel_data)` - 在指定位置绘制像素数据
- `handle_3_directive(layer_id, width, height, pixel_data)` - 设置图层数据
- `handle_4_directive(layer_id, src_x, src_y, src_width, src_height, dst_x, dst_y, target_color)` - 复杂图层操作
- `handle_5_directive(layer_id, width, height, file_path)` - 从文件加载数据
- `handle_6_directive(show_debug)` - 显示帧缓冲区
- `handle_7_directive(delay_ms)` - 延时指令
- `handle_1337_directive(layer_id, src_x, src_y, width, height)` - 特殊指令

### CIMGBuilder类

提供了一个方便的构建器类，支持链式调用：

```python
builder = CIMGBuilder(width, height)
builder.add_directive_1(w, h, data) \
       .add_directive_7(1000) \
       .add_directive_6(True) \
       .save("output.cimg")
```

### 辅助工具

- `create_test_pixel_data(width, height, color)` - 创建测试像素数据
- `create_exploit_cimg()` - 创建包含exploit的CIMG文件
- `create_simple_test_cimg()` - 创建简单测试文件

## 指令格式分析

基于反汇编代码分析，每个指令的二进制格式为：

### handle_1 (指令类型2)
- 2 bytes: 指令类型 (0x0002)
- 1 byte: 宽度
- 1 byte: 高度
- N bytes: RGBA像素数据 (width*height*4 bytes)

### handle_2 (指令类型3)
- 2 bytes: 指令类型 (0x0003)
- 1 byte: X坐标
- 1 byte: Y坐标
- 1 byte: 宽度
- 1 byte: 高度
- N bytes: RGBA像素数据

### handle_3 (指令类型4)
- 2 bytes: 指令类型 (0x0004)
- 1 byte: 图层ID
- 1 byte: 宽度
- 1 byte: 高度
- N bytes: 像素数据

### handle_4 (指令类型5)
- 2 bytes: 指令类型 (0x0005)
- 1 byte: 图层ID
- 1 byte: 源X坐标
- 1 byte: 源Y坐标
- 1 byte: 源宽度
- 1 byte: 源高度
- 1 byte: 目标X坐标
- 1 byte: 目标Y坐标
- 1 byte: 目标颜色

### handle_5 (指令类型6)
- 2 bytes: 指令类型 (0x0006)
- 1 byte: 图层ID
- 2 bytes: 宽高打包 (高8位|宽8位)
- N bytes: 文件路径字符串

### handle_6 (指令类型7)
- 2 bytes: 指令类型 (0x0007)
- 1 byte: 调试标志 (0/1)

### handle_7 (指令类型8)
- 2 bytes: 指令类型 (0x0008)
- 4 bytes: 延时毫秒数

### handle_1337 (指令类型1337)
- 2 bytes: 指令类型 (0x0539)
- 1 byte: 图层ID
- 1 byte: 源X坐标
- 1 byte: 源Y坐标
- 1 byte: 宽度
- 1 byte: 高度

## 使用示例

### 基本用法
```python
from main2 import *

# 创建像素数据
pixels = create_test_pixel_data(5, 5, (255, 0, 0, 255))

# 创建指令
directive = handle_1_directive(5, 5, pixels)

# 使用构建器
builder = CIMGBuilder(20, 20)
builder.add_directive_1(5, 5, pixels)
builder.save("output.cimg")
```

### 创建Exploit
```python
# 直接运行脚本会创建exploit CIMG文件
python3 main2.py
```

## 安全特性

这些指令接口特别适用于CTF和安全研究，因为：

1. `handle_4` 和 `handle_5` 可能存在缓冲区溢出漏洞
2. `handle_1337` 是特殊指令，可能用于信息泄露
3. 文件加载功能可能允许任意文件读取

## 测试

运行以下命令测试所有功能：

```bash
python3 main2.py  # 选择选项3查看所有可用指令
```

所有指令接口都已经过测试并能正确生成对应的二进制数据。
