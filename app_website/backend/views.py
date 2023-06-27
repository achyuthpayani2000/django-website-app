from django.contrib.auth.models import User

from .models import App
from backend.serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer,AddAppSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsAdminUser
class UserViewSet(viewsets.ModelViewSet):

    User=get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Allow any user to access GET requests
        elif self.request.method == 'POST':
            return [IsAuthenticated(),IsAdminUser()]  # Only authenticated users can create objects
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Additional logic for update requests (e.g., checking if the user is the owner)
            return [IsAdminUser(),IsAuthenticated()]
        elif self.request.method == 'DELETE':
            # Additional logic for delete requests (e.g., checking if the user is an admin)
            return [IsAuthenticated(),IsAdminUser()]

        return super().get_permissions()
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User created successfully.'}, status=HTTP_201_CREATED, headers=headers)

class CreateAppView(viewsets.ModelViewSet):
    queryset=App.objects.all()
    serializer_class = AddAppSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Allow any user to access GET requests
        elif self.request.method == 'POST':
            return [IsAuthenticated(),IsAdminUser()]  # Only authenticated users can create objects
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Additional logic for update requests (e.g., checking if the user is the owner)
            return [IsAdminUser(),IsAuthenticated()]
        elif self.request.method == 'DELETE':
            # Additional logic for delete requests (e.g., checking if the user is an admin)
            return [IsAuthenticated(),IsAdminUser()] 
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


