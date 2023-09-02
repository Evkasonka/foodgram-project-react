from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, object):
        return (request.method in SAFE_METHODS
                or object.author == request.user)
