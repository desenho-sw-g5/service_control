from abc import ABC, abstractmethod


class OnlyOne:
    def __init__(self):
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def remove(self, module):
        self.modules.remove(module)

    def call_func(self, func_name, *args, **kwargs):
        results = []

        for m in self.modules:
            if m.has_func(func_name):
                func = getattr(m, func_name)
                results.append(func(*args, **kwargs))

        return results


class InterfaceBunitinha(ABC):
    @abstractmethod
    def has_func(self, func_name: str) -> bool:
        pass


class UmModule(InterfaceBunitinha):
    def func_a(self):
        return "A"

    def func_b(self):
        return "B"

    def func_c(self):
        return "C"

    def has_func(self, func_name):
        return func_name == 'func_a' or func_name == 'func_b'

class DoisModule(InterfaceBunitinha):
    def func_b(self):
        return "Bbbbbb"

    def has_func(self, func_name):
        return func_name == 'func_b'

class TresModule(InterfaceBunitinha):
    def func_a(self):
        return "AaAaAaAAAa"

    def has_func(self, func_name):
        return func_name == 'func_a'

sing = OnlyOne()

m1 = UmModule()
m2 = DoisModule()
m3 = TresModule()

sing.add_module(m1)
sing.add_module(m2)
sing.add_module(m3)

dados = sing.call_func('func_a')
print(dados)

sing.remove(m3)

dados = sing.call_func('func_a')
print(dados)