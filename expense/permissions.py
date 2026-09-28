from rest_framework.permissions import BasePermission

class isOwner(BasePermission):
    #  allow only no admin users
   def has_permission(self, request, view):
      return bool(request.user and request.user.is_authenticated and request.user.is_staff==False) 