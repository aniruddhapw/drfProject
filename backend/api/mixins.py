from .permissions import IsStaffEditorPermisson
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes=[permissions.IsAdminUser,IsStaffEditorPermisson]
    