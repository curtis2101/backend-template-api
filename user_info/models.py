from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import string


User = get_user_model()


def generate_psw_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


class UserInfo(models.Model):
    user = models.ForeignKey(to=User, related_name='user_info', on_delete=models.CASCADE, null=True)
    reset_psw_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'

    @receiver(post_save, sender=User)
    def create_user_info(sender, instance, **kwargs):
        profile, created = UserInfo.objects.get_or_create(id=instance.id, user=instance)
        if created:
            profile.save()
