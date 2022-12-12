from django.contrib.auth.mixins import PermissionDenied, PermissionRequiredMixin


class OwnerPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().postAuthor.users.id == self.request.user.id:
            raise PermissionDenied()

        return self.request.user.has_perms(perms)
