class MyProperty:

    def __init__(self, fget=None, fset=None,
                 fdelete=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdelete = fdelete
        self.doc = doc

    def __get__(self, instance, owner):
        # 执行 @MyProperty 的时候
        # 被 MyProperty 装饰的 user_name 会赋值给 self.fget
        # 然后返回的 MyProperty(user_name) 会重新赋值给 user_name
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance, value):
        return self.fset(instance, value)

    def __delete__(self, instance):
        return self.fdelete(instance)

    def setter(self, func):
        # 调用 @user_name.setter，创建一个新的描述符
        # 其它参数不变，但是第二个参数 fset 变为接收的 func
        return type(self)(self.fget, func, self.fdelete, self.doc)

    def deleter(self, func):
        # 调用 @user_name.deleter，创建一个新的描述符
        # 其它参数不变，但是第三个参数 fdelete 变为接收的 func
        return type(self)(self.fget, self.fset, func, self.doc)


class Girl:

    def __init__(self):
        self.__name = None

    # user_name = MyProperty(user_name)
    # 调用时会触发描述符的 __get__
    @MyProperty
    def user_name(self):
        print("获取属性")
        return self.__name

    # 被一个新的描述符所代理，这个描述符实现了__set__
    # 给 g.user_name 赋值时，会触发 __set__
    @user_name.setter
    def user_name(self, value):
        self.__name = value

    # 被一个新的描述符所代理，这个描述符实现了 __delete__
    # 删除 g.user_name 时，会触发 __delete__
    @user_name.deleter
    def user_name(self):
        print("属性被删了")
        del self.__name


g = Girl()
print(g.user_name)  # None
g.user_name = "satori"
print(g.user_name)  # satori
del g.user_name  # 属性被删了

# 当然啦，user = MyProperty(...) 这种方式也是支持的

print(Girl.__dict__)
