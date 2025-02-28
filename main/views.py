from django.http import JsonResponse
from django.views.generic import TemplateView

from main.KVM import KVMManager
from main.mixins import AuthenticationMixin

from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_authenticated:

        return redirect('/index')
    else:
        return redirect("accounts/log-in")

# def start_hypervisor(request,domain_name):
#     print(f"Received request to start: {domain_name}")
#     data = {}
#     try:
#         if request.user.is_authenticated:
#             manager= KVMManager()
#             domain= manager.get_domain(domain_name)
#             print(domain)
#
#             if domain:
#                 initial_state = domain.get_state()
#                 print(f"Domain {domain_name} initial state: {initial_state}")  # Debug log
#                 domain.start()
#                 new_state = domain.get_state()
#                 logger.info(f"Domain {domain_name} state after start attempt: {new_state}")
#                 print(f"Domain {domain_name} state after start attempt: {new_state}")
#                 data['response'] = 1
#                 data['new_status'] = 'Running'
#                 data['message'] = f'{domain_name} started successfully'
#             else:
#
#                 data['response'] = 0
#                 data['error'] ="Hypervisor not found"
#     except Exception as e:
#         data["response"] = 0
#         data["error"] = str(e)
#         error_message = f"An error occurred while starting {domain_name}: {str(e)}"
#
#     return JsonResponse(data)
def start_hypervisor(request, domain_name):
    print(f"Received request to start: {domain_name}")
    data = {}

    try:
        if request.user.is_authenticated:
            manager = KVMManager()
            domain = manager.get_domain(domain_name)

            if domain:
                initial_state = domain.get_state()
                print(f"Domain {domain_name} initial state: {initial_state}")

                result = domain.start()  # Check if this returns a success/failure value
                print(result)
                new_state = domain.get_state()
                print(f"Domain {domain_name} state after start attempt: {new_state}")

                if new_state.lower() == "running":  # Ensure the domain actually started
                    data['response'] = 1
                    data['new_status'] = 'Running'
                    data['message'] = f'{domain_name} started successfully'
                else:
                    data['response'] = 0
                    data['error'] = f"Failed to start {domain_name}, current state: {new_state}"
                    logger.error(f"Failed to start {domain_name}, current state: {new_state}")

            else:
                data['response'] = 0
                data['error'] = "Hypervisor not found"
                logger.error("Hypervisor not found")

    except Exception as e:
        error_message = f"An error occurred while starting {domain_name}: {str(e)}"
        data["response"] = 0
        data["error"] = error_message
        logger.error(error_message)
        print(error_message)

    return JsonResponse(data)

# def stop_hypervisor(request,domain_name):
#     print(f"Received request to stop: {domain_name}")
#     data = {}
#     try:
#         if request.user.is_authenticated:
#             manager= KVMManager()
#             domain = manager.get_domain(domain_name)
#
#             if domain:
#                 domain.stop()
#                 data['response'] = 1
#                 data['message'] = f'{domain_name} stopped successfully'
#             else:
#
#                 data['response'] = 0
#                 data['error'] = "Hypervisor not found"
#
#     except Exception as e:
#         data["response"] = 0
#         data["error"] = str(e)
#         error_message = f"An error occurred while stopping {domain_name}: {str(e)}"
#     return JsonResponse(data)
def stop_hypervisor(request, domain_name):
    print(f"Received request to stop: {domain_name}")
    data = {}

    try:
        if request.user.is_authenticated:
            manager = KVMManager()
            domain = manager.get_domain(domain_name)

            if domain:
                initial_state = domain.get_state()
                print(f"Domain {domain_name} initial state: {initial_state}")

                result = domain.stop()  # Check if this returns a success/failure value
                print(f"Stop result: {result}")

                new_state = domain.get_state()
                print(f"Domain {domain_name} state after stop attempt: {new_state}")

                if new_state.lower() == "shut off":  # Ensure the domain actually stopped
                    data['response'] = 1
                    data['new_status'] = 'Shut Off'
                    data['message'] = f'{domain_name} stopped successfully'
                else:
                    data['response'] = 0
                    data['error'] = f"Failed to stop {domain_name}, current state: {new_state}"
                    logger.error(f"Failed to stop {domain_name}, current state: {new_state}")

            else:
                data['response'] = 0
                data['error'] = "Hypervisor not found"
                logger.error("Hypervisor not found")

    except Exception as e:
        error_message = f"An error occurred while stopping {domain_name}: {str(e)}"
        data["response"] = 0
        data["error"] = error_message
        logger.error(error_message)
        print(error_message)

    return JsonResponse(data)


def restart_hypervisor(request, domain_name):
    print(f"Received request to restart: {domain_name}")
    data = {}
    try:
        if request.user.is_authenticated:
            manager = KVMManager()
            domain = manager.get_domain(domain_name)
            if domain:
                domain.stop()  # First, stop the domain
                domain.start()  # Then, start it again
                data['response'] = 1
                data['message'] = f'{domain_name} restarted successfully'
            else:
                data['response'] = 0
                data['error'] = "Hypervisor not found"
    except Exception as e:
        data["response"] = 0
        data["error"] = str(e)

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