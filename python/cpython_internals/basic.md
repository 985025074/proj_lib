# 元类
## 类型对象（class 这个type）：
有一部分工作留到了运行时进行。这一节很复杂，暂时跳过。76
## 类的创建：
1. 类本省是一个code object.
2. 其次，code object的 co_const 带上所有的类内函数。
3. 在模块中 通过load build class 来创建.
## 类的property vs 函数静态变量
函数局部变量存在f_localplus，编译期间决定分配大小。所以跟类的动态是两种实现机制。
## metaclass 
### __new__ + __init__:
下面__new__函数根据cls 对象返回实例对象给__init__函数，也就是所谓的self
```py
class A:

    def __new__(cls, *args, **kwargs):
        print("__new__")
        # 这里的参数 cls 就表示 A 这个类本身
        # object.__new__(cls) 便是根据 cls 创建 cls 的实例对象
        return object.__new__(cls)

    def __init__(self):
        # 然后执行 __init__，里面的 self 指的就是实例对象
        # 执行 __init__ 时，__new__ 的返回值会自动作为参数传递给 self
        print("__init__")

A()
"""
__new__
__init__
"""

```
## metaclass:
```py
# type 接收三个参数：类名、继承的基类、属性
class A(list):
    name = "古明地觉"

# 上面这个类翻译过来就是
A = type("A", (list,), {"name": "古明地觉"})
print(A)  # <class '__main__.A'>
print(A.__name__)  # A
print(A.__base__)  # <class 'list'>
print(A.name)  # 古明地觉

```

metaclass就是一种type。
```py
class MyType(type):
    def __new__(mcs, name, bases, attr):
        print(name)
        print(bases)
        print(attr)

# 指定 metaclass，表示 A 这个类由 MyType 创建
# 我们说 __new__ 是为实例对象开辟内存的
# 那么 MyType 的实例对象是谁呢？显然就是这里的 A
# 因为 A 指定了 metaclass 为 MyType，所以 A 的类型就是 MyType
class A(int, object, metaclass=MyType):
    name = "古明地觉"
"""
A
(<class 'int'>, <class 'object'>)
{'__module__': '__main__', '__qualname__': 'A', 'name': '古明地觉'}
"""
# 我们看到一个类在创建的时候会向元类的 __new__ 中传递三个值
# 分别是类名、继承的基类、类的属性
# 但此时 A 并没有被创建出来
print(A)  # None

```
metaclass的__new__返回类的实例对象。也就是说，返回具体的A（比如有个classA）
attr负责类的所有方法+属性
###  __prepare__
必须是@classmethod,**返回的对象将会被并入attr**
```py
class MyType(type):
    def __new__(mcs, name, bases, attr):
        print(name)
        print(bases)
        print(attr)

# 指定 metaclass，表示 A 这个类由 MyType 创建
# 我们说 __new__ 是为实例对象开辟内存的
# 那么 MyType 的实例对象是谁呢？显然就是这里的 A
# 因为 A 指定了 metaclass 为 MyType，所以 A 的类型就是 MyType
class A(int, object, metaclass=MyType):
    name = "古明地觉"
"""
A
(<class 'int'>, <class 'object'>)
{'__module__': '__main__', '__qualname__': 'A', 'name': '古明地觉'}
"""
# 我们看到一个类在创建的时候会向元类的 __new__ 中传递三个值
# 分别是类名、继承的基类、类的属性
# 但此时 A 并没有被创建出来
print(A)  # None

```
### __init __subclass

```py

class Base:

    def __init_subclass__(cls, **kwargs):
        print(cls)
        print(kwargs)

# 当类被创建的时候，会触发其父类的__init_subclass__
class A(Base):
    pass
"""
<class '__main__.A'> 
{}
"""

class B(Base, name="古明地觉", age=16):
    pass

"""
<class '__main__.B'> 
{'name': '古明地觉', 'age': 16}
"""

```
类似元类的一种东西。 不同之处，元类在__new__无法访问子类。但是init_class可以访问实际的类（参数cls

```py
class Base:

    def __init_subclass__(cls, **kwargs):
        for k, v in kwargs.items():
            setattr(cls, k, v)

class A(Base, name="古明地觉", age=16,
        __str__=lambda self: "hello world"):
    pass


print(A.name, A.age)  # 古明地觉 16
print(A())  # hello world

```
# mro_entries:
继承实例对象返回的类型。

```py
class Base:

    def __init_subclass__(cls, **kwargs):
        for k, v in kwargs.items():
            setattr(cls, k, v)

class A(Base, name="古明地觉", age=16,
        __str__=lambda self: "hello world"):
    pass


print(A.name, A.age)  # 古明地觉 16
print(A())  # hello world

```

# descriptor:
```py
 __get__、__set__、__delete__  三个方法出现其中一个

```
```py
class Descriptor:

    def __get__(self, instance, owner):
        print("__get__")
        print(instance)
        print(owner)

    def __set__(self, instance, value):
        print("__set__")
        print(instance)
        print(value)


class Girl:
    # 此时的 name 属性就被描述符代理了
    name = Descriptor()

    def __init__(self, name, age):
        self.name = name
        self.age = age

g = Girl("satori", 16)
"""
__set__
<__main__.Girl object at 0x0000021D8D225E40>
satori
"""

```
## dict详细解释：
```py
class A:
    def add(self):
        return 1 + 1
    
a = A()
print(A.__dict__)
print(a.__dict__)
```
注意 方法是在类的dict，而不是实例的dict
## 优先级
数据描述符：__set__
非数据：不带set的
非数据优先级< 实例属性 < 数据描述符 < 类属性
类属性可以覆写描述符属性。也就是通过class.Des = ..可以覆写掉整个描述符，子类将无法再使用描述符。
## 实例和类 都可以访问同一个描述符，区别是instance 是否None

## 
```py
class Descriptor:
    def __get__(self, instance, owner):
        print("Getting value")
        return "value"
    def __set__(self, instance, value):
        print("Setting value")
        instance.name = value


class A:
    name = Descriptor()



a = A()

a. name = 123
print(a.__dict__)
```
无限循环。
注意设置属性最好这样>instance.__dict__[]= xxx
或者设置到描述符上面
## set_name onwer是类，name 是属性名
```py
class Descriptor:

    def __get__(self, instance, owner):
        return instance.__dict__["name"]

    def __set__(self, instance, value):
        instance.__dict__["name"] = value

    def __set_name__(self, owner, name):
        print(owner)
        print(name)


class Girl:
    age = Descriptor()

"""
<class '__main__.Girl'>
age
"""

```



## 有意思，type checker:
```py
class TypeChecker:

    def __init__(self, name, excepted_type):
        self.name = name
        self.excepted_type = excepted_type

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.excepted_type):
            tp = type(value).__name__
            excepted_tp = self.excepted_type.__name__
            raise TypeError(f"{self.name} 接收的值应该是 {excepted_tp} 类型，而不是 {tp} 类型")

        instance.__dict__[self.name] = value


def type_checker(cls):
    # cls 就是要被 type_checker 装饰的类
    # 拿到 __init__ 函数
    __init__ = getattr(cls, "__init__", None)
    # 如果 __init__ 为空，或者它不是一个函数，那么直接将类返回
    if __init__ is None or not hasattr(__init__, "__code__"):
        return cls

    # 拿到 __init__ 函数的 __annotations__
    annotations = cls.__init__.__annotations__
    # 进行遍历，给类设置被描述符代理的属性
    for name, excepted_type in annotations.items():
        setattr(cls, name, TypeChecker(name, excepted_type))
    return cls


# 以后在创建类的时候，直接打上这个装饰器就行了
# 但是显然这个装饰器依赖类型注解
# 如果没有类型注解的话，那么该属性是不会被代理的
@type_checker
class Girl:

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

try:
    g = Girl(16, 16)
except TypeError as e:
    print(e)  # name 接收的值应该是 str 类型, 而不是 int 类型

```
### 实现中出现的错误:
```py
class EmptyClass:
    ...
# print(EmptyClass.__dict__)
class TypeChecker:
    def __init__(self, expected_type: type):
        self.expected_type = expected_type

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Hope to get {self.expected_type},but get {type(value)}")
        else:
            # print(type(instance))
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str):
        self.class_type = owner
        self.name = name


def type_check(cls:type)->type:
    
    __init__ = cls.__init__
    try:
        init_annotation = __init__.__annotations__
    except:
        return cls
    _dict_ = {
        k:v  for k,v in cls.__dict__.items() if k not in EmptyClass.__dict__
    }
    for k,v in init_annotation.items():
        _dict_[k] = TypeChecker(v)
        ...
        
    return type(cls.__name__,cls.__bases__,_dict_)    


@type_check
class Test:
    def __init__(self,name:str,age:int):
        self.name = name
        self.age = age
print(Test.__dict__)
Test()


```
显示descriptor __dict__ can apply to test.
这是因为把旧的mapproxy discriptor 带到新的类了，所以报错。
推测 mapproxy中有一些特别的检查》 
# method vs func:
```py
<function Test.class_func at 0x73c5c4c41300>
<bound method Test.class_func of <__main__.Test object at 0x73c5c4dff5f0>>
```
注意A.fuc 和 a.func的重要区别，原因是对于func是个描述符，会判断当前是有什么调用的，实例调用会有包装。
# classmethod底层实现原理。
classmethod是一个内置函数。
会进行类似make_method的绑定操作。
只不过，绑定的是类。与普通a.method别无二至。

# class vs module:
