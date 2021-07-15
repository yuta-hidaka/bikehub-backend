from company.models import CompanyUserGroup
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ProductEditableOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, _, obj):
        if request.method in SAFE_METHODS:
            return True

        group = CompanyUserGroup.objects.filter(
            user=request.user,
            company=obj.company
        ).first()
        return True if group and group.permission <= CompanyUserGroup.Permissions.EDITOR else False
