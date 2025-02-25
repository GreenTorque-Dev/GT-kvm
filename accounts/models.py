from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    type_to_confirm = models.BooleanField(default=True)
    services_stopped = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    timezone = models.CharField(max_length=63, default='UTC')

class Activation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    user_type_choices = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    user_type = models.CharField(max_length=10, choices=user_type_choices, default='user')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    mfa_token = models.CharField(max_length=20, unique=True, default='')

    @classmethod
    def save_mfa_token(cls, user, mfa_token):
        # Generate a new MFA token
        activation, created = cls.objects.get_or_create(user=user)
        activation.mfa_token = mfa_token
        activation.save()

    @classmethod
    def get_activation_data_for_user(cls, user):
        try:
            activation = cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None  # Or raise an exception if you prefer

        user_data = {
            'user_id': activation.user_id,
            'created_at': activation.created_at,
            'code': activation.code,
            'email': activation.email,
            'last_login_ip': activation.last_login_ip,
            'mfa_token': activation.mfa_token,
        }
        return user_data