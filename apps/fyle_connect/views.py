from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from apps.fyle_connect.models import FyleAuth
from apps.fyle_connect.utils import FyleOAuth2
from apps.xero_workspace.models import Workspace, FyleCredential
from fyle_xero_integration_web_app.settings import FYLE_BASE_URL


class FyleAuthoriseView(View, LoginRequiredMixin):
    """
    Fyle Connect view
    """
    template_name = "fyle_connect/source_connect.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        is_connected = FyleCredential.objects.filter(workspace__id=workspace_id).exists()
        context = {"source": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name, "is_connected": is_connected}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        value = request.POST.get('type')
        if value == 'connect':
            fyle_oauth = FyleOAuth2()
            return redirect(fyle_oauth.authorise(str(workspace_id)))
        if value == 'disconnect':
            FyleAuth.objects.get(id=FyleCredential.objects.get(workspace__id=workspace_id).id).delete()
            return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)


class FyleTokenView(View, LoginRequiredMixin):
    """
    Exchange code for token and redirect to workspace URL using state
    """

    def get(self, request):
        code = request.GET.get('code')
        workspace_id = request.GET.get('state')
        if code is not None and workspace_id is not None:
            fyle_oauth = FyleOAuth2()
            tokens = fyle_oauth.get_tokens(code)
            access_token = tokens.get('access_token')
            refresh_token = tokens.get('refresh_token')
            if access_token is not None and refresh_token is not None:
                fyle_auth = FyleAuth.objects.create(url=FYLE_BASE_URL, refresh_token=refresh_token)
                FyleCredential.objects.create(fyle_auth=fyle_auth, workspace=Workspace.objects.get(id=workspace_id))
        return redirect(f'/workspace/{workspace_id}/source')
