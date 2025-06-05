

from typing import Dict
import unittest


class UnittestMetaClass(type):
    test_func = []

    @classmethod
    def call_test(cls):
        for test in cls.test_func:
            try:
                test()
            except AssertionError as e:
                print(
                    f"Test failed: {test.from_class}.{test.test_name} - {e} , from file:{e.__traceback__.tb_frame.f_code.co_firstlineno}")

    def __new__(mcs, name, bases, attrs: Dict):

        # add self.assert:
        final_class = super().__new__(mcs, name, bases, attrs)
        final_class_instance = final_class()
        # Modify the class creation process
        for k, v in attrs.items():
            if callable(v) and k.startswith('test_'):
                def wrapped_test():
                    return v(final_class_instance)
                metainfo = {
                    "from_class": name,
                    "test_name": k,
                }
                wrapped_test.__dict__.update(metainfo)
                mcs.test_func.append(wrapped_test)
        return final_class


class Impl(metaclass=UnittestMetaClass):
    def assertEqual(self, a, b):
        assert a == b, f"Expected {a} to equal {b}"
    ...


class FirstTest(Impl):
    def test_a(self):
        self.assertEqual(1, 2)


if __name__ == "__main__":
    UnittestMetaClass.call_test()
