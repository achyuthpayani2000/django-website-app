from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User=get_user_model()

class IsAdminUser(BasePermission):
    
    """
    Custom permission class to allow only admin users access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='admin'


