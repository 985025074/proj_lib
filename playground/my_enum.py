class MyEnumImpl:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyEnumImpl({self.value})"

class MyEnumMeta(type):
    def __getattr__(cls, name):
        if name in cls.__dict__:
            value = cls.__dict__[name]
            if not isinstance(value, MyEnumImpl):
                wrapped = MyEnumImpl(value)
                setattr(cls, name, wrapped)  # 缓存起来
                return wrapped
        raise AttributeError(f"No such enum: {name}")

class MyEnum(metaclass=MyEnumMeta):
    pass

class TestMyEnum(MyEnum):
    nihao = 123

print(TestMyEnum.nihao)  # ✅ 输出: MyEnumImpl(123)
