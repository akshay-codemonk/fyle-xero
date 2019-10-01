from apps.xero_workspace.models import Workspace


def workspace_data(request):
    """
    Context processor for navbar
    :param request:
    :return: workspace name and id
    """
    if request.user.is_authenticated:
        try:
            workspace_id = request.resolver_match.kwargs.get('workspace_id')
            workspace = Workspace.objects.get(id=workspace_id)
            return {'workspace_id': workspace_id, 'workspace_name': workspace.name}
        except Workspace.DoesNotExist:
            return {}
    return {}
