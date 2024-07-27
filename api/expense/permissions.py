from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsCategoryOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.created_by.id == request.user.id
