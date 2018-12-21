from rest_framework import permissions


class ISOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 安全请求被允许
        if request.method in permissions.SAFE_METHODS:
            return True
        # 用户一致则允许，否则返回错误
        return obj.owner == request.user
