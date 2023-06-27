from backend.models import CustomUser,App
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','password','email','role','id','username']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AddAppSerializer(serializers.ModelSerializer):
    class Meta:
        model=App
        fields='__all__'  
          


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    default_error_messages = {
        'no_active_account': 'No active account found with the given credentials'
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom fields to the token payload
        token['email'] = user.email
        token['password'] = user.password
        token['role']=user.role
        # Add any other custom fields
        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = User.objects.filter(email=credentials['email']).first()

            if user and user.check_password(credentials['password']):
                if not user.is_active:
                    raise serializers.ValidationError(
                        self.error_messages['no_active_account'],
                        code='no_active_account'
                    )

                data = {
                    'access': str(self.get_token(user).access_token)
                }

                return data
        
        raise serializers.ValidationError(
                self.error_messages['no_active_account'],
                code='no_active_account'
            )