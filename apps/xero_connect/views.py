from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from apps.xero_connect.utils import XeroOAuth2
from apps.xero_connect.models import XeroAuth
from apps.xero_workspace.models import XeroCredential, Workspace
from fyle_xero_integration_web_app.settings import XERO_BASE_URL, XERO_CLIENT_ID, \
    XERO_CLIENT_SECRET


class DestinationView(View):
    """
    Destination (xero) view
    """
    template_name = "xero_connect/destination.html"

    def get(self, request, workspace_id):
        connected = XeroCredential.objects.filter(workspace__id=workspace_id).exists()
        context = {"destination": "active", "connected": connected,
                   "settings_tab": "active"}
        return render(request, self.template_name, context)


class XeroConnectView(View):
    """
    Xero (destination) connect view
    """

    @staticmethod
    def post(request, workspace_id):
        xero_oauth = XeroOAuth2()
        return redirect(xero_oauth.authorize(str(workspace_id)))


class XeroDisconnectView(View):
    """
    Xero (destination) disconnect view
    """

    @staticmethod
    def post(request, workspace_id):
        XeroAuth.objects.get(id=XeroCredential.objects.get(workspace__id=workspace_id).id).delete()
        return HttpResponseRedirect(reverse('xero_workspace:destination', args=[workspace_id]))


class XeroTokenView(View):
    """
    Exchange code for token and redirect to workspace URL using state
    """

    @staticmethod
    def get(request):
        code = request.GET.get('code')
        workspace_id = request.GET.get('state')
        if code is not None and workspace_id is not None:
            xero_oauth = XeroOAuth2()
            tokens = xero_oauth.get_tokens(code)
            access_token = tokens.get('access_token')
            refresh_token = tokens.get('refresh_token')
            if access_token is not None and refresh_token is not None:
                xero_auth = XeroAuth.objects.create(
                    url=XERO_BASE_URL,
                    client_id=XERO_CLIENT_ID,
                    client_secret=XERO_CLIENT_SECRET,
                    refresh_token=refresh_token
                )
                XeroCredential.objects.create(xero_auth=xero_auth, 
                                              workspace=Workspace.objects.get(id=workspace_id))
        return HttpResponseRedirect(reverse('xero_workspace:destination', args=[workspace_id]))
