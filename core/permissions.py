from rest_framework.permissions import BasePermission
from .models import Organization

class HasAPIKey(BasePermission):
    """
    Allows access only to requests that include a valid X-API-KEY header.
    """
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return False
        
        # Check if the key exists, and attach the organization to the request for later use
        try:
            organization = Organization.objects.get(api_key=api_key)
            request.organization = organization
            return True
        except Organization.DoesNotExist:
            return False
