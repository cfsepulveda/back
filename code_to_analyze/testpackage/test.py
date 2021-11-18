class ExampleClass1(object):
    class_variable1 = 5
    class_variable2 = 6

    def func1(self):
        self.instance_variable = 6

        def inner_func(b):
            return b + 5

        local_variable = self.class_variable1

        return local_variable

    def func2(self):
        print(self.class_variable2)

    @staticmethod
    def func3(variable):
        return variable + 7

class ExampleClass2(object):
    def func1(self):
        self.instance_variable1 = 7