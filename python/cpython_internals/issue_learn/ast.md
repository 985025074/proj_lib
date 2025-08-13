# https://github.com/python/cpython/issues/135801
# 问题出自：
```C
static int
codegen_check_compare(compiler *c, expr_ty e)
{
    // the passed e is a Compare node
    Py_ssize_t i, n;
    bool left = check_is_arg(e->v.Compare.left);
    expr_ty left_expr = e->v.Compare.left;
    // 可能有多个 比较运算符，compare 包括 a<b<c这种串行的狮子
    n = asdl_seq_LEN(e->v.Compare.ops);
    for (i = 0; i < n; i++) {
        cmpop_ty op = (cmpop_ty)asdl_seq_GET(e->v.Compare.ops, i);
        expr_ty right_expr = (expr_ty)asdl_seq_GET(e->v.Compare.comparators, i);
        bool right = check_is_arg(right_expr);
        // 如果监测到 is 或 is not 的比较运算符，并且op 是 is 或 is not
        if (op == Is || op == IsNot) {
            if (!right || !left) {
                // ！（right and left） 如果两侧有一侧是常量，输出错误
                const char *msg = (op == Is)
                        ? "\"is\" with '%.200s' literal. Did you mean \"==\"?"
                        : "\"is not\" with '%.200s' literal. Did you mean \"!=\"?";
                expr_ty literal = !left ? left_expr : right_expr;
                return _PyCompile_Warn(
                    c, LOC(e), msg, infer_type(literal)->tp_name
                );
            }
        }
        left = right;
        left_expr = right_expr;
    }
    return SUCCESS;
}

```
# dive into _PyCompile_Warn
```C
* Emits a SyntaxWarning and returns 0 on success.
   If a SyntaxWarning raised as error, replaces it with a SyntaxError
   and returns -1.
*/
int
_PyCompile_Warn(compiler *c, location loc, const char *format, ...)
{
    va_list vargs;
    va_start(vargs, format);
    PyObject *msg = PyUnicode_FromFormatV(format, vargs);
    va_end(vargs);
    if (msg == NULL) {
        return ERROR;
    }
    int ret = _PyErr_EmitSyntaxWarning(msg, c->c_filename, loc.lineno, loc.col_offset + 1,
                                       loc.end_lineno, loc.end_col_offset + 1);
    Py_DECREF(msg);
    return ret;
}

```
```C

void
_PyErr_RaiseSyntaxError(PyObject *msg, PyObject *filename, int lineno, int col_offset,
                        int end_lineno, int end_col_offset)
{
    //出错的 代码文件
    PyObject *text = PyErr_ProgramTextObject(filename, lineno);
    if (text == NULL) {
        text = Py_NewRef(Py_None);
    }
    // 错误的参数
    PyObject *args = Py_BuildValue("O(OiiOii)", msg, filename,
                                   lineno, col_offset, text,
                                   end_lineno, end_col_offset);
    if (args == NULL) {
        goto exit;
    }
    // 设置异常，设置到当前线程状态
    PyErr_SetObject(PyExc_SyntaxError, args);
 exit:
    Py_DECREF(text);
    Py_XDECREF(args);
}
```
大概就在这里了，
其中：
```
O - 表示一个Python对象（PyObject*）
(OiiOii) - 表示一个元组，包含：

O - Python对象
i - 整数（int）
i - 整数（int）
O - Python对象
i - 整数（int）
i - 整数（int）



所以整个格式字符串表示：构建一个包含两个元素的元组，第一个元素是Python对象（msg），第二个元素是一个包含6个子元素的元组（filename, lineno, col_offset, text, end_lineno, end_col_offset）。
```
那么有趣的来了，这个过滤错误的模块设置是在哪个环节出来的呢？
gdb 调试得知：
```C
* Like PyErr_WarnExplicitObject, but automatically sets up context */
int
_PyErr_WarnExplicitObjectWithContext(PyObject *category, PyObject *message,
                                     PyObject *filename, int lineno)
{
    PyObject *unused_filename, *module, *registry;
    int unused_lineno;
    int stack_level = 1;

    if (!setup_context(stack_level, NULL, &unused_filename, &unused_lineno,
                       &module, &registry)) {
        return -1;
    }


    int rc = PyErr_WarnExplicitObject(category, message, filename, lineno,
                                      module, registry);
    Py_DECREF(unused_filename);
    Py_DECREF(registry);
    Py_DECREF(module);
    return rc;
}
```
```C
/* Like PyErr_WarnExplicitObject, but automatically sets up context */
int
_PyErr_WarnExplicitObjectWithContext(PyObject *category, PyObject *message,
                                     PyObject *filename, int lineno)
{
    PyObject *unused_filename, *module, *registry;
    int unused_lineno;
    int stack_level = 1;

    if (!setup_context(stack_level, NULL, &unused_filename, &unused_lineno,
                       &module, &registry)) {
        return -1;
    }


    int rc = PyErr_WarnExplicitObject(category, message, filename, lineno,
                                      module, registry);
    Py_DECREF(unused_filename);
    Py_DECREF(registry);
    Py_DECREF(module);
    return rc;
}

```

进 setupcontext里看看。
```C
 /* Setup module. */
    rc = PyDict_GetItemRef(globals, &_Py_ID(__name__), module);
    if (rc < 0) {
        goto handle_error;
    }
    if (rc > 0) {

        if (Py_IsNone(*module) || PyUnicode_Check(*module)) {
            return 1;
        }
        Py_DECREF(*module);
    }

    *module = PyUnicode_FromString("<string>");
    if (*module == NULL) {
        goto handle_error;
    }
```
~~只是单纯找了一下module的名字，看来问题在下个函数：~~ gdb 测试发现，从setupcontext module 就是sys了。
让我从上面看看

# gdb 调试发现：
是这里扔出来的异常
```
         if (rc < 0)
            goto handle_error;
    }

    /* Setup module. */
    rc = PyDict_GetItemRef(globals, &_Py_ID(__name__), module);
    if (rc < 0) {
        goto handle_error;
    }
    
    if (rc > 0) {

```
# 原因大白，
```C
    }
    PyInterpreterState *interp = tstate->interp;
    PyFrameObject *f = PyThreadState_GetFrame(tstate);
    // Stack level comparisons to Python code is off by one as there is no
    // warnings-related stack level to avoid.
    if (stack_level <= 0 || is_internal_frame(f)) {
        while (--stack_level > 0 && f != NULL) {
            PyFrameObject *back = PyFrame_GetBack(f);
            Py_SETREF(f, back);
        }
    }
    else {
        while (--stack_level > 0 && f != NULL) {
            f = next_external_frame(f, skip_file_prefixes);
        }
    }

    if (f == NULL) {
        globals = interp->sysdict;
        *filename = PyUnicode_FromString("<sys>");
        *lineno = 0;
    }
```

setupcontext里 因为还在编译时期，所以运行正是NULL，自动搞了一个sys来。
<<<<<<< HEAD
=======


>>>>>>> 38578d7 (...sth save)
