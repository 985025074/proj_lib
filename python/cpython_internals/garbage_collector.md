# 垃圾收集器探索文章

## gc 模块开始

基本函数：
- gc.enable .disable .isenable
- collect
- get_objects(generation number )跟踪对象
- get_stats() 统计数据
- is_tracked(ob)

## 垃圾收集器作用机制

翻译自：gc.set_threshold的文档：

总共有三代。每次survice collection的 进入下一代。thresh hold作用。当 allocation - dealloc 阈值的时候，就会进行collection


## 从 object 说起：
说起object 我们直接来看pyobject.

代码地址：Include/object.h

```C
struct _object {
    _Py_ANONYMOUS union {
#if SIZEOF_VOID_P > 4
        PY_INT64_T ob_refcnt_full; /* This field is needed for efficient initialization with Clang on ARM */
        struct {
#  if PY_BIG_ENDIAN
            uint16_t ob_flags;
            uint16_t ob_overflow;
            uint32_t ob_refcnt;
#  else
            uint32_t ob_refcnt;
            uint16_t ob_overflow;
            uint16_t ob_flags;
#  endif
        };
#else
        Py_ssize_t ob_refcnt;
#endif
        _Py_ALIGNED_DEF(_PyObject_MIN_ALIGNMENT, char) _aligner;
    };

    PyTypeObject *ob_type;
};
```

so 所以实际上 只有一个union 内装refcnt + ob_type  
那么任务很明确 要研究垃圾收集器。就要研究refcnt_减少的时机，我们去看看ref_cnt的引用。

### 操纵refcount的家伙

代码地址：  Include/refcount.h

```C
static inline Py_ALWAYS_INLINE void Py_INCREF(PyObject *op)
{
#if defined(Py_LIMITED_API) && (Py_LIMITED_API+0 >= 0x030c0000 || defined(Py_REF_DEBUG))
    // Stable ABI implements Py_INCREF() as a function call on limited C API
    // version 3.12 and newer, and on Python built in debug mode. _Py_IncRef()
    // was added to Python 3.10.0a7, use Py_IncRef() on older Python versions.
    // Py_IncRef() accepts NULL whereas _Py_IncRef() doesn't.
#  if Py_LIMITED_API+0 >= 0x030a00A7
    _Py_IncRef(op);
#  else
    Py_IncRef(op);
#  endif
#else
    // Non-limited C API and limited C API for Python 3.9 and older access
    // directly PyObject.ob_refcnt.
#if defined(Py_GIL_DISABLED)
    uint32_t local = _Py_atomic_load_uint32_relaxed(&op->ob_ref_local);
    uint32_t new_local = local + 1;
    if (new_local == 0) {
        _Py_INCREF_IMMORTAL_STAT_INC();
        // local is equal to _Py_IMMORTAL_REFCNT_LOCAL: do nothing
        return;
    }
    if (_Py_IsOwnedByCurrentThread(op)) {
        _Py_atomic_store_uint32_relaxed(&op->ob_ref_local, new_local);
    }
    else {
        _Py_atomic_add_ssize(&op->ob_ref_shared, (1 << _Py_REF_SHARED_SHIFT));
    }
#elif SIZEOF_VOID_P > 4
    PY_UINT32_T cur_refcnt = op->ob_refcnt;
    if (cur_refcnt >= _Py_IMMORTAL_INITIAL_REFCNT) {
        // the object is immortal
        _Py_INCREF_IMMORTAL_STAT_INC();
        return;
    }
    op->ob_refcnt = cur_refcnt + 1;
#else
    if (_Py_IsImmortal(op)) {
        _Py_INCREF_IMMORTAL_STAT_INC();
        return;
    }
    op->ob_refcnt++;
#endif
    _Py_INCREF_STAT_INC();
#ifdef Py_REF_DEBUG
    // Don't count the incref if the object is immortal.
    if (!_Py_IsImmortal(op)) {
        _Py_INCREF_IncRefTotal();
    }
#endif
#endif
}

```

好吧 代码太多了，说实话

真正重要的是这里的Py_dealoc一族。
  
```C
static inline Py_ALWAYS_INLINE void Py_DECREF(PyObject *op)
{
    // Non-limited C API and limited C API for Python 3.9 and older access
    // directly PyObject.ob_refcnt.
    if (_Py_IsImmortal(op)) {
        _Py_DECREF_IMMORTAL_STAT_INC();
        return;
    }
    _Py_DECREF_STAT_INC();
    if (--op->ob_refcnt == 0) {
        _Py_Dealloc(op);
    }
}

```

py_deloc:

```C

/*
When deallocating a container object, it's possible to trigger an unbounded
chain of deallocations, as each Py_DECREF in turn drops the refcount on "the
next" object in the chain to 0.  This can easily lead to stack overflows.
To avoid that, if the C stack is nearing its limit, instead of calling
dealloc on the object, it is added to a queue to be freed later when the
stack is shallower */
# 注释的意思是 释放不是无限制的。因为可能会栈溢出。因此这里有一个队列来临时存放过多的释放
void
_Py_Dealloc(PyObject *op)
{
    PyTypeObject *type = Py_TYPE(op);
    unsigned long gc_flag = type->tp_flags & Py_TPFLAGS_HAVE_GC;
    destructor dealloc = type->tp_dealloc;
    PyThreadState *tstate = _PyThreadState_GET();
    intptr_t margin = _Py_RecursionLimit_GetMargin(tstate);
    if (margin < 2 && gc_flag) {
        _PyTrash_thread_deposit_object(tstate, (PyObject *)op);
        return;
    }
#ifdef Py_DEBUG
#if !defined(Py_GIL_DISABLED) && !defined(Py_STACKREF_DEBUG)
    /* This assertion doesn't hold for the free-threading build, as
     * PyStackRef_CLOSE_SPECIALIZED is not implemented */
    assert(tstate->current_frame == NULL || tstate->current_frame->stackpointer != NULL);
#endif
    PyObject *old_exc = tstate != NULL ? tstate->current_exception : NULL;
    // Keep the old exception type alive to prevent undefined behavior
    // on (tstate->curexc_type != old_exc_type) below
    Py_XINCREF(old_exc);
    // Make sure that type->tp_name remains valid
    Py_INCREF(type);
#endif

#ifdef Py_TRACE_REFS
    _Py_ForgetReference(op);
#endif
    _PyReftracerTrack(op, PyRefTracer_DESTROY);
    (*dealloc)(op);

#ifdef Py_DEBUG
    // gh-89373: The tp_dealloc function must leave the current exception
    // unchanged.
    if (tstate != NULL && tstate->current_exception != old_exc) {
        const char *err;
        if (old_exc == NULL) {
            err = "Deallocator of type '%s' raised an exception";
        }
        else if (tstate->current_exception == NULL) {
            err = "Deallocator of type '%s' cleared the current exception";
        }
        else {
            // It can happen if dealloc() normalized the current exception.
            // A deallocator function must not change the current exception,
            // not even normalize it.
            err = "Deallocator of type '%s' overrode the current exception";
        }
        _Py_FatalErrorFormat(__func__, err, type->tp_name);
    }
    Py_XDECREF(old_exc);
    Py_DECREF(type);
#endif
    if (tstate->delete_later && margin >= 4 && gc_flag) {
        此处的意思应该是 距离极值还远 因此可以继续删除
        _PyTrash_thread_destroy_chain(tstate);
    }
}

```
似乎。。没有那么复杂？？

查看一下gc 模块的位置：

在 Python 中，内置模块（如 `gc`、`sys`、`os` 等）的实现通常分为两部分：  
1. **Python 层面的接口定义**：部分模块会有 `.py` 文件定义高层接口（如函数、类的声明）。  
2. **C 语言底层实现**：核心功能（尤其是涉及内存管理、系统交互的模块）通常由 C 语言实现，编译后嵌入 Python 解释器中。  


以 **`gc` 模块**（垃圾回收模块）为例，其定义位置如下：  

### 1. C 语言核心实现（主要逻辑）  
`gc` 模块的核心功能由 C 语言编写，代码位于 Python 源码的 `Modules/gcmodule.c` 文件中。  
这里实现了垃圾回收的核心算法（如分代回收、标记-清除机制）、C 层面的函数（如 `gc_collect`、`gc_enable` 等），以及向 Python 暴露的模块接口。  


### 2. Python 层面的接口封装（可选）  
部分模块会在 `Lib/` 目录下有对应的 `.py` 文件，用于封装 C 接口或添加高层逻辑。  
但 `gc` 模块比较特殊，其 Python 层面的接口直接由 C 代码导出，没有单独的 `Lib/gc.py` 文件。  
其他模块（如 `sys`）的 Python 层面定义在 `Lib/sys.py`，但核心功能仍在 C 代码中（`Python/sysmodule.c`）。  


### 总结  
内置模块的“定义位置”取决于具体模块：  
- 核心逻辑（尤其是涉及解释器底层的模块，如 `gc`、`sys`）主要在 **`Modules/` 目录下的 `.c` 文件**中实现。  
- 部分模块会在 **`Lib/` 目录下有 `.py` 文件**，用于补充高层接口或纯 Python 实现。  

如果你想查看 `gc` 模块的源码，可以访问 Python 官方仓库（如 [cpython/Modules/gcmodule.c](https://github.com/python/cpython/blob/main/Modules/gcmodule.c)）。

## 那么gc 是一个内建模块吗？ 直接print 果然是的

```
 ./python
Python 3.15.0a0 (heads/main:c22cc8fccd, Sep  4 2025, 16:04:49) [GCC 15.2.1 20250813] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print(gc_
KeyboardInterrupt
>>> import gc
>>> print(gc)
<module 'gc' (built-in)>
## 
```

## 一个小程序的分析

```py
import dis

def func_to_dis():
    import gc
    import another 

dis.dis(func_to_dis)
```

字节码

```raw
❯ ./python TestForShiyicong/test.py
  3           RESUME                   0

  4           LOAD_SMALL_INT           0
              LOAD_CONST               1 (None)
              IMPORT_NAME              0 (gc)
              STORE_FAST               0 (gc)
 
  5           LOAD_SMALL_INT           0
              LOAD_CONST               1 (None)
              IMPORT_NAME              1 (another)
              STORE_FAST               1 (another)
              LOAD_CONST               1 (None)
              RETURN_VALUE  解释每条治疗
```
RESUME： 恢复执行
LOAD_SMALL_INT:小蒸熟吃


可见 import_name就是关键

## 再探
发现generated_cases.h这个文件 在python/下面

根据注释 现在python的超级大case 已经变成是自动撰写的了。是一个工具// This file is generated by Tools/cases_generator/tier1_generator.py 
所写的。

他说是根据 bytecode.c 这个文件写的。

点开这个文件 更有意思的东西：

```C
// This file contains instruction definitions.
// It is read by generators stored in Tools/cases_generator/
// to generate Python/generated_cases.c.h and others.
// Note that there is some dummy C code at the top and bottom of the file
// to fool text editors like VS Code into believing this is valid C code.
// The actual instruction definitions start at // BEGIN BYTECODES //.
// See Tools/cases_generator/README.md for more information.
```
有意思，为什么要这样呢.

~~今天就先写道这里了。~~

两个重要文件 generated_cases.h 和 bytecode.c

## internal_doc of garbage_collctor  

the below function can be used to get the reference count of any object . always bigger than 1. 因为本身会带来一次引用

```python
    sys.getrefcount(object)

```

有一个例子：

```python
>>> container = []
>>> container.append(container)
>>> sys.getrefcount(container)
3
>>> del container

```

文档说这删不掉，那么我们看看del的代码吧。
先来看看del对应字节码是什么

```C
>>> dis.dis(func)
  1           RESUME                   0

  2           LOAD_CONST               1 (1)
              STORE_FAST               0 (a)

  3           DELETE_FAST              0 (a)
              RETURN_CONST             0 (None)
>>> 


```

delete_Fast:

```C
        TARGET(DELETE_FAST) {
            // #if Py_TAIL_CALL_INTERP
            // int opcode = DELETE_FAST;
            // (void)(opcode);
            // #endif
            frame->instr_ptr = next_instr;
            next_instr += 1;
            INSTRUCTION_STATS(DELETE_FAST);
            _PyStackRef v = GETLOCAL(oparg);
            if (PyStackRef_IsNull(v)) {
                _PyFrame_SetStackPointer(frame, stack_pointer);
                _PyEval_FormatExcCheckArg(tstate, PyExc_UnboundLocalError,
                    UNBOUNDLOCAL_ERROR_MSG,
                    PyTuple_GetItem(_PyFrame_GetCode(frame)->co_localsplusnames, oparg)
                );
                stack_pointer = _PyFrame_GetStackPointer(frame);
                JUMP_TO_LABEL(error);
            }
            _PyStackRef tmp = GETLOCAL(oparg);
            GETLOCAL(oparg) = PyStackRef_NULL;
            _PyFrame_SetStackPointer(frame, stack_pointer);
            PyStackRef_XCLOSE(tmp);
            stack_pointer = _PyFrame_GetStackPointer(frame);
            DISPATCH();
        }
```

代码说明：

经过一番探索 证明 在`PyStackRef_XCLOSE(tmp);`是仅仅进行当基数为0删除的。
而上面`getlocal..` 则说明了 找不到变量 也就是NameError的来源：栈里的指针没了。

```C
static inline void Py_DECREF_MORTAL(PyObject *op)
{
    assert(!_Py_IsStaticImmortal(op));
    _Py_DECREF_STAT_INC();
    if (--op->ob_refcnt == 0) {
        _Py_Dealloc(op);
    }
}

```

GC 头部：

```raw
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ \ |                    *_gc_next                  | | +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ | PyGC_Head
                  |                    *_gc_prev                  | |
    object -----> +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ /
                  |                    ob_refcnt                  | \
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ | PyObject_HEAD
                  |                    *ob_type                   | |
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ /
                  |                      ...                      |
```

这里的gcnext 和 prev 就是双指针节点的意思

# 代码中造成cylic的情况有

Exceptions contain traceback objects that contain a list of frames that contain the exception itself.
Module-level functions reference the module's dict (which is needed to resolve globals), which in turn contains entries for the module-level functions.
Instances have references to their class which itself references its module, and the module contains references to everything that is inside (and maybe other modules) and this can lead back to the original instance.
When representing data structures like graphs, it is very typical for them to have internal links to themselves.
