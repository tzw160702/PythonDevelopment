# !/usr/bin/env python3
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    """ 权限限制 """
    message = '你无权访问'

    def has_permission(self, request, view):
        # 只有 VIP 用户才可以访问
        if request.user.user_type != 2:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """对某个对象的访问权限"""
        pass


