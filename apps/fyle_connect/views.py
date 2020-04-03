from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.fyle_connect.models import FyleAuth
from apps.fyle_connect.utils import FyleOAuth2
from apps.xero_workspace.models import Workspace, FyleCredential
from fyle_xero_integration_web_app.settings import FYLE_BASE_URL


class SourceView(View):
    """
    Fyle (source) connect view
    """
    template_name = "fyle_connect/source.html"

    def get(self, request, workspace_id):
        connected = FyleCredential.objects.filter(workspace__id=workspace_id).exists()
        context = {"source": "active", "connected": connected,
                   "settings_tab": "active"}
        return render(request, self.template_name, context)


class FyleConnectView(View):
    """
    Fyle (source) connect view
    """

    @staticmethod
    def post(request, workspace_id):
        fyle_oauth = FyleOAuth2()
        return redirect(fyle_oauth.authorise(str(workspace_id)))


class FyleDisconnectView(View):
    """
    Fyle (source) disconnect view
    """

    @staticmethod
    def post(request, workspace_id):
        FyleAuth.objects.get(id=FyleCredential.objects.get(workspace__id=workspace_id).fyle_auth.id).delete()
        return HttpResponseRedirect(reverse('xero_workspace:source', args=[workspace_id]))


class FyleTokenView(View):
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
        return HttpResponseRedirect(reverse('xero_workspace:source', args=[workspace_id]))
