from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.app_settings import PasswordResetSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from password_reset.serializers import ResetPasswordCodeSerializer, CustomPasswordResetForm
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _

# Get the UserModel
UserModel = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'new_password1', 'new_password2',
    ),
)


class PasswordCustomResetView(GenericAPIView):
    """
        Calls Django Auth PasswordResetForm save method.

        Accepts the following POST parameters: email
        Returns the success/fail message.
        """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        # Return the success message with OK HTTP status
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class ResetPasswordCodeValidate(GenericAPIView):
    """
    Validate the User reset password code sent to his email

    response returns uid and token that need to be passed to reset
    password confirmation request to identify the user for security reasons
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['code'],
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The reset password code sent to the user\'s email'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Code has been confirmed.'
                    ),
                    'uid': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='The user ID encoded as a URL-safe string'
                    ),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='The token needed to reset the user\'s password'
                    )
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Code cannot be confirmed.'
            )
        }
    )
    def post(self, request, *args, **kwargs):

        serializer = ResetPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        if code:
            user = UserModel.objects.filter(user_info__reset_psw_code=code).first()
            if user:
                # Generate the uid and token
                uid = user_pk_to_url_str(user)
                token = default_token_generator.make_token(user)

                # Create the response
                response_data = {
                    'message': 'Code has been confirmed.',
                    'uid': uid,
                    'token': token,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response('Code cannot be confirmed.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Code not provided.', status=status.HTTP_400_BAD_REQUEST)
