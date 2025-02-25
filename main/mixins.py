from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import HttpResponseRedirect
from app import config

from accounts.models import Activation


class AuthenticationMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:log_in"))
        try:
            activation = Activation.objects.get(user=request.user)
            mfa_token = activation.mfa_token
            signup_date = activation.created_at

            # if not mfa_token and signup_date + timedelta(days=config.MIN_MFA_DAY_ALLOW) <= now():
            #     return HttpResponseRedirect(reverse("accounts:set_mfa"))

        except Activation.DoesNotExist:
            return HttpResponseRedirect(reverse("accounts:set_mfa"))

        return super().dispatch(request, *args, **kwargs)
