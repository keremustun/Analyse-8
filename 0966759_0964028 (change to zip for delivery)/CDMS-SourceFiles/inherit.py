
class BaseClass():
    def __init__(self):
        self.x = 10
    def Func(self):
        print(self.x)

class DerivedClass(BaseClass):
    def __init__(self):
        self.a = BaseClass().x
        self.x = 11
    
    def Func(self):
        c = BaseClass()
        c.Func()
        print(self.a)
        print(self.x)

BaseClass().Func()
print(DerivedClass().a)
print(DerivedClass().x)