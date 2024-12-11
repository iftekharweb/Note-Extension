from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import serializers

from core.models import User


import os
from dotenv import load_dotenv
load_dotenv()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=255,
        style = {'input_type':'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password == password2:
            return data
        raise serializers.ValidationError("Password and Confirm Password Did Not Match!")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UseLogInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta: 
        model = User
        fields = ['email', 'password']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.context.get('user')

        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        if old_password == new_password:
            raise serializers.ValidationError("New password must be different from old password.")
        user.set_password(new_password)
        user.save()
        return data
    

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        else:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = os.environ.get('BASE_URL')+'/api/send-reset-password-email/'+uid+'/'+token
            print(link)
            # I M P L E M E N T   S E N D   E M A I L 


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        style={'input_type':'password'},
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={'input_type':'password'},
        write_only=True
    )
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password Did Not Match!")

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token Is Not Valid Or Expired!!')
            
            user.set_password(password)
            user.save()
            return data
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator(user, token)
            raise serializers.ValidationError('Token Is Not Valid Or Expired!!')