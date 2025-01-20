from django.contrib.auth.models import Group
from rest_framework import permissions

# HERE PERMISSIONS.PY


# ● _is_in_group
def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """

    # _PIN_  related_name='primary_users' 
    #   for reverse lookups I will need to use primary_users instead of the default user_set

    try:
        return Group.objects.get(name=group_name).auth_group.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


# ● _has_group_permission
def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


# ✪ ⋙ ── ── ── IsAdminUser ── ── ── ──➤
class IsAdminUser(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin','super']

    def has_permission(self, request, view):
        
        # ○ _has_group_permission
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

    def has_object_permission(self, request, view, obj):
        
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

