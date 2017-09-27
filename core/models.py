from django.db import models
from django.contrib.auth.models import User

from core.enums import RoleEnum, ModuleEnum

class Module(models.Model):
    name = models.CharField(
        max_length=30,
        choices=ModuleEnum.choices(),
        default=ModuleEnum.MY_PROFILE,
        unique=True)

    def __str__(self):
        return "%s" % self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=RoleEnum.choices(), default=RoleEnum.MEMBER.name)
    modules = models.ManyToManyField(Module, related_name='profiles', blank=True)

    def __str__(self):
        print(self.role)

        return "%s: %s" % (self.role, self.user.username)
