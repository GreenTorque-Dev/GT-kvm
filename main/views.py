from django.http import JsonResponse
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

def start_hypervisor(request,domain_name):
    print(f"Received request to start: {domain_name}")
    data = {}
    try:
        if request.user.is_authenticated:
            manager= KVMManager()
            domain= manager.get_domain(domain_name)
            if domain:
                domain.start()
                data['response'] = 1
                data['message'] = f'{domain_name} started successfully'
            else:

                data['response'] = 0
                data['error'] ="Hypervisor not found"
    except Exception as e:
        data["response"] = 0
        data["error"] = str(e)
        error_message = f"An error occurred while starting {domain_name}: {str(e)}"

    return JsonResponse(data)



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
# test