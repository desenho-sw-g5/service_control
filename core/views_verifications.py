from django.http import Http404, HttpRequest
from django.core.urlresolvers import resolve
from abc import ABCMeta, abstractmethod
from typing import Iterable

from core.models import Module
from core.enums import ModuleEnum

import logging

logger = logging.getLogger('django_test')

# Composite Component
class ViewVerification(metaclass=ABCMeta):
    @abstractmethod
    def verify(self, request: HttpRequest) -> bool:
        """
        It executes a verification based on the data on the given request.
        """
        pass


#Composite
class ViewVerificator(ViewVerification):

    def __init__(self):
        self._verifications = []

    def add(self, verification: ViewVerification):
        if verification is not None:
            self._verifications.append(verification)

    def verify(self, request: HttpRequest) -> bool:
        is_valid = True

        for verification in self._verifications:
            is_valid = verification.verify(request)

            if not is_valid:
                break

        return is_valid


# Composite Leaf
class ModuleAccessVerification(ViewVerification):

    def verify(self, request: HttpRequest) -> bool:
        user = request.user

        if user.is_anonymous():
            return False

        profile = user.profile
        module = request.__getattribute__('module')

        return profile.modules.filter(name=module.name).exists()


# Composite Leaf
class LoginRequiredVerification(ViewVerification):

    def verify(self, request: HttpRequest) -> bool:
        return request.user.is_authenticated()


# Django URL Decorator
class ViewsVerificationsDecorator(object):
    """
    Recives a module and some verifications
    Apply the verifications before calling the requested view

    OBS: The order of the given verifications MATTER !
    """

    def __init__(self, module: ModuleEnum,
                    verifications: Iterable[ViewVerification],
                    unless: Iterable[str] = []):
        self._module = module
        self._verifications = verifications
        self._unless = unless

    def get_request(self, *args) -> HttpRequest:
        request = None

        for arg in args:
            if isinstance(arg, HttpRequest):
                request = arg
                break

        if request is None:
            raise ValueError("HttpRequest not found")

        return request

    def __call__(self, view):
        verificator = ViewVerificator()

        for verification in self._verifications:
            verificator.add(verification)


        def wrapper(*args, **kwargs):
            request = self.get_request(*args)
            request.__setattr__('module', self._module)
            current_url = resolve(request.path_info).url_name

            if current_url in self._unless:
                logger.debug(
                    "URL Verifications: {} in unless, skip validations" \
                    .format(current_url))

                return view(*args, **kwargs)
            elif verificator.verify(request):
                logger.debug(
                    "URL Verifications: User has access to {}, sending view" \
                    .format(current_url))

                return view(*args, **kwargs)
            else:
                logger.debug(
                    "URL Verifications: User DONT has access to {}, sending 404 view" \
                    .format(current_url))

                raise Http404("Could access the page")

        return wrapper
