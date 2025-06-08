import ctypes
import os

now_dir = __file__
father_dir = os.path.dirname(now_dir)
print(father_dir)
lib_dir = os.path.join(father_dir,"mylib")
clib = ctypes.CDLL(lib_dir)

clib.func()
