from enum import Enum, unique as unique_enum_values
from typing import Iterable, Tuple


@unique_enum_values
class RoleEnum(Enum):
    ADMIN = 'Admin'
    MANAGER = 'Manager'
    MEMBER = 'Member'

    @classmethod
    def choices(cls) -> Iterable[Tuple[str, str]]:
        """
        Returns a iterable of tuples with RoleEnum (name, value)
        """
        return tuple((e.name, e.value) for e in cls)

    def __str__(self):
        return self.value



@unique_enum_values
class ModuleEnum(Enum):
    MY_PROFILE = 'MyProfile'

    @classmethod
    def choices(cls) -> Iterable[Tuple[str, str]]:
        """
        Returns a iterable of tuples with RoleEnum (name, value)
        """
        return tuple((e.name, e.value) for e in cls)

    def __str__(self):
        return self.value
