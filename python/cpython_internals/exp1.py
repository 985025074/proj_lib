class TypeChecker:
    def __init__(self, expected_type: type):
        self.expected_type = expected_type

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Hope to get {self.expected_type},but get {type(value)}")
        else:
            print(type(instance))
            print(instance.__dict__)
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set_name__(self, owner: type, name: str):
        self.class_type = owner
        self.name = name

def type_check(cls:type)->type:
    __init__ = cls.__init__
    init_annotation = __init__.__annotations__
    _dict_ = dict(cls.__dict__.items())

    for k,v in init_annotation.items():
        assert isinstance(v,type)
        _dict_[k] = TypeChecker(v)

        ...

    R =  type("new_type",cls.__bases__,_dict_)    

    return R

@type_check
class Test:
    def __init__(self,name:str,age:int):
        self.name = name
        self.age = age

class 


