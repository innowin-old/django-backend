from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import permissions

from .models import Organization, MetaData


class StaffOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (
                    request.user == obj.staff_organization.owner or request.user == obj.staff_organization.admins or request.user.is_superuser):
                return False
        return False


class StaffCountOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (
                    request.user == obj.staff_count_organization.owner or request.user == obj.staff_count_organization.admins or request.user.is_superuser):
                return False
        return False


class PictureOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj and (
                    request.user == obj.picture_organization.owner or request.user == obj.picture_organization.admins or request.user.is_superuser):
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
            if obj and (
                    request.user == obj.customer_organization.owner or request.user == obj.customer_organization.admins or request.user.is_superuser):
                return False
        return False


class ConfirmationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.confirmation_corroborant.identity_user == request.user or obj.confirmation_confirmed.identity_user == request.user or request.user.is_superuser:
            return True
        return False


class IsOrganizationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            try:
                organization = Organization.objects.get(Q(owner=request.user) | Q(admins__in=request.user))
            except ObjectDoesNotExist:
                return False
        return True


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