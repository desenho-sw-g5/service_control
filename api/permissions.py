#from rest_framework.permissions import BasePermission

#from core.enums import ProfileRole

#class IsMember(BasePermission):
#    """
#    Allows access only to member profiles
#    """
#
#    def has_permission(self, request, view):
#        if not request.user:
#            return False
#
#        profile = request.user.profile
#
#        return profile.role == ProfileRole.Member.Admin
