from django.views.generic import TemplateView

from main.KVM import KVMManager
from main.mixins import AuthenticationMixin

from django.shortcuts import render, redirect

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_authenticated:

        return redirect('/index')
    else:
        return redirect("accounts/log-in")


class IndexPageView(AuthenticationMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        manager = KVMManager()
        domains = manager.list_domains()
        hypervisors = []
        for domain_name in domains:
            domain = manager.get_domain(domain_name)
            hypervisors.append({
                'name': domain.name,
                'state': domain.get_state(),
                'config': domain.get_config()
            })
        context['hypervisors'] = hypervisors
        return context
