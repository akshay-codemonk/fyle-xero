from django.core.exceptions import PermissionDenied

from apps.xero_workspace.models import Workspace


def is_workspace_user(function):
    """
    Checks if the user belongs to the requested workspace
    :param function:
    :return:
    """

    def wrap(request, *args, **kwargs):
        try:
            workspace_id = kwargs.get('workspace_id')
            if workspace_id is None:
                return function(request, *args, **kwargs)
            workspace_users = Workspace.objects.get(id=workspace_id).user.all()
            if request.user not in workspace_users:
                raise PermissionDenied
            return function(request, *args, **kwargs)
        except:
            raise PermissionDenied

    return wrap
