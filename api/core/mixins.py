from rest_framework.viewsets import ViewSetMixin

class ActionPermissionMixin(ViewSetMixin):
    permission_classes_by_action = {}
    def get_permissions(self):
        if self.action in self.permission_classes_by_action:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        return [permission() for permission in self.permission_classes_by_action["default"]]