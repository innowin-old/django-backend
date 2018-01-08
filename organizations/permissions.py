from rest_framework import permissions

class StaffOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (request.user == obj.staff_organization.owner or request.user == obj.staff_organization.admins or request.user.is_superuser):
                return False
        return False


class StaffCountOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (request.user == obj.staff_count_organization.owner or request.user == obj.staff_count_organization.admins or request.user.is_superuser):
                return False
        return False


class PictureOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (request.user == obj.picture_organization.owner or request.user == obj.picture_organization.admins or request.user.is_superuser):
                return False
        return False


class FollowOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.follow_identity.identity_user == request.user or obj.follow_follower.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class CustomerOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (request.user == obj.customer_organization.owner or request.user == obj.customer_organization.admins or request.user.is_superuser):
                return False
        return False

class ConfirmationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.confirmation_corroborant.identity_user == request.user or obj.confirmation_confirmed.identity_user == request.user or request.user.is_superuser:
            return True
        return False