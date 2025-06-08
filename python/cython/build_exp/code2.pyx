
cdef extern from "code2_impl.h":
    double cfib(int n)


def fib_with_c(n):
    """调用 C 编写的斐波那契数列"""
    return cfib(n)
