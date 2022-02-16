from rest_framework.permissions import BasePermission


class HasApiRequest(BasePermission):
    def has_permission(self, request, view):
        headers = request.headers
        perm_api = PermApi()
        perm_api.set_header(headers)

        return perm_api.execute()


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        headers = request.headers

        return True


class FilterHeaders:
    header = {}

    def set_header(self, header):
        self.header = header

    def get_headers(self):
        return self.header

    def execute(self):
        pass


class PermApi(FilterHeaders):
    def execute(self):
        if 'Token-api' in self.get_headers():
            return True

        return False