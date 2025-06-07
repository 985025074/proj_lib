import dis


class A:
    asdasd = 223
    def __init__(self):
        self.a = 123
        pass
    
print(A.__dict__)
print(A().__dict__)
print(int.__add__)