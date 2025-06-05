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

