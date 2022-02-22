from typing import Type


class MyInterface:
    def m(self) -> None:
        pass


class MyClass1(MyInterface):
    def m(self):
        print("It's me, MyClass1")


class MyClass2(MyInterface):
    def m(self):
        print("It's me, MyClass2")


def generic_method(x: MyInterface) -> None:
    x.m()


def create_instance(class_object: Type[MyInterface]) -> MyInterface:
    x: MyInterface = class_object()
    x.m()
    return x


print(type(create_instance(MyClass1)))
print(type(create_instance(MyClass2)))

print(type(MyClass1))


# reveal_locals() # let mypy type checker output inferred types
# more types here https://realpython.com/python-type-checking/
