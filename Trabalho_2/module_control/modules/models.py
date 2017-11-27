from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from abc import ABC, abstractmethod
from importlib import import_module
import json


class Module(ABC):
    @abstractmethod
    def has_action(action: str) -> bool:
        pass


class ModuleStorageObserver(ABC):
    @abstractmethod
    def modules_changed(self):
        pass


class ModuleStorageSubject:
    @abstractmethod
    def notify_observers(self):
        pass


class ModuleStorage(models.Model, ModuleStorageSubject):
    modules = models.TextField(default="[]")

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ModuleStorage, self).save(*args, **kwargs)
        self.notify_observers()


    def delete(self, *args, **kwargs):
        pass

    def notify_observers(self):
        mc = ModuleControl()
        mc.modules_changed()

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def get_modules_path(self):
        ms = ModuleStorage.objects.first()
        data = json.loads(ms.modules)
        return data


class ModuleControl(ModuleStorageObserver):
    __instance = None

    def __new__(cls):
        if ModuleControl.__instance is None:
            ModuleControl.__instance = object.__new__(cls)

            ModuleControl.__instance.modules = []
            ModuleControl.__instance.module_storage = ModuleStorage.load()
            ModuleControl.__instance.modules_changed()

        return ModuleControl.__instance

    def modules_changed(self):
        self.modules = []

        for path_and_module in self.module_storage.get_modules_path():
            path_and_module = path_and_module.split(".")
            path = ".".join(path_and_module[:-1])
            module_name = "".join(path_and_module[-1:]).replace("\r", "")

            try:
                module = import_module(path)
                kclass = getattr(module, module_name)
                self.modules.append(kclass())
            except Exception as err:
                print("="*80)
                print("Modulo nao encontrado")
                print(err)
                print("="*80)

    def call_action(self, action: str, *args, **kwargs):
        results = []

        for m in self.modules:
            if m.has_action(action):
                fn_action = getattr(m, action)
                results.append(fn_action(*args, **kwargs))

        return results


#@receiver(post_save, sender=ModuleStorage)
#def on_module_storage_updated(**kwargs):
#    mc = ModuleControl()
#    mc.modules_changed()