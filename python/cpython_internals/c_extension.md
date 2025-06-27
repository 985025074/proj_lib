# 从 C 扩展出发：
必须的头文件：
```py
#define PY_SSIZE_T_CLEAN
#include <Python.h>
```
# exmple:
```C

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}
```
# 异常处理：
```py
最常用的就是 PyErr_SetString()。 其参数是异常对象和 C 字符串。 异常对象一般是像 PyExc_ZeroDivisionError 这样的预定义对象。 C 字符串指明异常原因，并被转换为一个 Python 字符串对象存储为异常的“关联值”。

另一个有用的函数是 PyErr_SetFromErrno() ，仅接受一个异常对象，异常描述包含在全局变量 errno 中。最通用的函数还是 PyErr_SetObject() ，包含两个参数，分别为异常对象和异常描述。你不需要使用 Py_INCREF() 来增加传递到其他函数的参数对象的引用计数。

你可以通过 PyErr_Occurred() 在不造成破坏的情况下检测是否设置了异常。 这将返回当前异常对象，或者如果未发生异常则返回 NULL。 你通常不需要调用 PyErr_Occurred() 来查看函数调用中是否发生了错误，因为你应该能从返回值中看出来。
```

## 清楚异常：
```
想要忽略由一个失败的函数调用所设置的异常，异常条件必须通过调用 PyErr_Clear() 显式地被清除。 C 代码应当调用 PyErr_Clear() 的唯一情况是如果它不想将错误传给解释器而是想完全由自己来处理它（可能是尝试其他方法，或是假装没有出错）。

最后，当你返回一个错误指示器时要注意清理垃圾（通过为你已经创建的对象执行 Py_XDECREF() 或 Py_DECREF() 调用）！
```
