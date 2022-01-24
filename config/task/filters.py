from rest_framework.filters import BaseFilterBackend


class IsOwnerFilterBackend(BaseFilterBackend):
    """"Custom filter for filter_backends=[...]"""

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user.id)
