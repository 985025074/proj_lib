class my_classmethod:
    def __init__(self,func):
        self.inner_func = func
    def __get__(self,instance,owner):
        def class_method(*args,**kwargs):
            return self.inner_func(owner,*args,**kwargs)
        return class_method
class A:
    a_ = 123
    @my_classmethod
    def print(cls):
        print(type(cls))
        return cls.a_
    
print(A.print())