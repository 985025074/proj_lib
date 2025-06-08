
# from Cython.Build.Dependencies import cythonize
# from setuptools import setup
# # 我们说构建扩展模块的过程分为两步: 
# # 1）将 Cython 代码翻译成 C 代码; 
# # 2）根据 C 代码生成扩展模块
# # 第一步要由 Cython 编译器完成, 通过 cythonize; 
# # 第二步要由 distutils 完成, 通过 distutils.core 下的 setup
# setup(ext_modules=cythonize("code1.pyx", language_level=3))
# # 里面还有一个参数 language_level=3 
# # 表示只需要兼容 Python3 即可，而默认是 2 和 3 都兼容
# # 如果你是 Python3 环境，那么建议加上这个参数

# # cythonize 负责将 Cython 代码转成 C 代码
# # 然后 setup 根据 C 代码生成扩展模块



from Cython.Build.Dependencies import cythonize
from setuptools import setup,Extension
# 我们说构建扩展模块的过程分为两步: 
# 1）将 Cython 代码翻译成 C 代码; 
# 2）根据 C 代码生成扩展模块
# 第一步要由 Cython 编译器完成, 通过 cythonize; 
# 第二步要由 distutils 完成, 通过 distutils.core 下的 setup
ext = Extension(name="target_code2",sources=["code2_impl.c","code2.pyx"])
setup(ext_modules=cythonize(ext, language_level=3))
# 里面还有一个参数 language_level=3 
# 表示只需要兼容 Python3 即可，而默认是 2 和 3 都兼容
# 如果你是 Python3 环境，那么建议加上这个参数

# cythonize 负责将 Cython 代码转成 C 代码
# 然后 setup 根据 C 代码生成扩展模块
