from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _
import user_info.models
from user_info.models import UserInfo

if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import (filter_users_by_email, user_username)

# Get the UserModel
UserModel = get_user_model()


# override the allauth reset password form
class CustomPasswordResetForm(AllAuthPasswordResetForm):
    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        # If no user exists with given email address, fail silently
        if not len(self.users):
            raise serializers.ValidationError(_("The e-mail address is not assigned"
                                                " to any user account"))
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):

        email = self.cleaned_data['email']

        for user in self.users:
            # generating a reset password code
            code = user_info.models.generate_psw_code()
            # getting the user
            user_obj = UserInfo.objects.get(user=user)
            # saving the code to the user reset_psw_code field
            user_obj.reset_psw_code = code
            # saving the UserInfo instance
            user_obj.save()

            context = {
                'user': user,
                'code': code,
                'request': request,
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['user'] = user_username(user)
            get_adapter().send_mail('account/email/password_reset_key', email, context)

        return email


# override the allauth serializer
class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = CustomPasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value


class ResetPasswordCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
