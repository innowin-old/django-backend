from rest_framework import permissions

class OrganizationOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj and request.user == obj.owner:
      return True

    return False
