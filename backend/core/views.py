from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import renderers


# M A N U A L L Y   G E N E R A T E   T O K E N
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [renderers.UserRenderer]

    def post(self, request, format=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response(
            {
                'token':token,
                'msg':'Registration Successful !'
            }, 
            status=status.HTTP_201_CREATED
        ) 
    

class UserLogInView(APIView):
    renderer_classes = [renderers.UserRenderer]

    def post(self, request, format=None):
        serializer = serializers.UseLogInSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        'token': token,
                        'msg':'LogIn Successful !'
                    }, 
                    status=status.HTTP_200_OK
                )
            else :
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    

class UserChangePasswordView(APIView):
    renderer_classes = [renderers.UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.UserChangePasswordSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'msg':'Change of Password Is Successful !'
            }, 
            status=status.HTTP_200_OK
        )
    

class SendPasswordResetEmailView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, format=None):
        serializer = serializers.SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'msg':'Reset Password link Has Been Sent! Please, Check Your Email!'
            }, 
            status=status.HTTP_200_OK
        )
    


class UserPasswordResetView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = serializers.UserPasswordResetSerializer(
            data=request.data,
            context={'uid':uid, 'token': token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'msg':'Reset of Password Is Successfull!'
            }, 
            status=status.HTTP_200_OK
        )