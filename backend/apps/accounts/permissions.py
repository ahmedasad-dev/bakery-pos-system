from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import BasePermission

from .models import active_membership


class HasOrganizationPermission(BasePermission):
    """Base permission for views that set `required_organization_permission`."""

    organization_header = "HTTP_X_ORGANIZATION_ID"

    def has_permission(self, request, view):
        organization_id = request.META.get(self.organization_header)
        if not organization_id:
            raise NotFound("X-Organization-ID header is required.")

        membership = active_membership(request.user, organization_id)
        if membership is None:
            raise NotFound("Organization was not found.")

        permission_code = getattr(view, "required_organization_permission", None)
        if permission_code and not membership.has_permission(permission_code):
            raise PermissionDenied("You do not have permission to perform this action.")

        request.organization = membership.organization
        request.membership = membership
        return True

