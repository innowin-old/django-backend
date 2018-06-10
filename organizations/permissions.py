from rest_framework import permissions

from users.models import Identity
from .models import Organization


class IsStaffOrganizationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            organization_id = request.POST.get('staff_organization', None)
            if organization_id is not None:
                try:
                    organization_obj = Organization.objects.get(pk=organization_id)
                except Organization.DoesNotExist:
                    return False
                if organization_obj.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if request.user == obj.staff_organization.owner or request.user == obj.staff_organization.admins or request.user.is_superuser:
                return True
        return True


class IsStaffCountOrganizationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            organization_id = request.POST.get('staff_count_organization', None)
            if organization_id is not None:
                try:
                    organization_obj = Organization.objects.get(pk=organization_id)
                except Organization.DoesNotExist:
                    return False
                if organization_obj.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if request.user == obj.staff_count_organization.owner or request.user in obj.staff_count_organization.admins or request.user.is_superuser:
                return False
        return True


class IsPictureOrganizationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            organization_id = request.POST.get('picture_organization', None)
            if organization_id is not None:
                try:
                    organization_obj = Organization.objects.get(pk=organization_id)
                except Organization.DoesNotExist:
                    return False
                if organization_obj.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if request.user == obj.picture_organization.owner or request.user == obj.picture_organization.admins or request.user.is_superuser:
                return False
        return False


class FollowOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.follow_identity.identity_user == request.user or obj.follow_follower.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class IsCustomerOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if request.user == obj.customer_organization.owner or request.user in obj.customer_organization.admins or request.user.is_superuser:
                return False
        return True


class IsConfirmationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if 'confirm_flag' not in request.POST or request.user.is_superuser:
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            if obj.confirm_flag is False and request.POST.get('confirm_flag') is True:
                confirmed_identity = Identity.objects.get(pk=obj.confirmation_confirmed.id)
                if confirmed_identity.identity_user is not None:
                    if confirmed_identity.identity_user == request.user or request.user.is_superuser:
                        return True
                else:
                    if confirmed_identity.identity_organization.owner == request.user or request.user.is_superuser:
                        return True
        if obj.confirmation_corroborant.identity_user == request.user or obj.confirmation_confirmed.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class IsMetaDataOrganizationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            organization_id = request.POST.get('meta_organization')
            if organization_id.isdigit():
                try:
                    organization = Organization.objects.get(pk=organization_id)
                except Organization.DoesNotExist:
                    return False
                if organization.owner == request.user or request.user.is_superuser:
                    return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if obj.meta_organization.owner == request.user or request.user.is_superuser:
            return True
        return False