from django.urls import path, include
from rest_framework import routers
from backend.views import CustomTokenObtainPairView, UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),
)


urlpatterns = [
    path('',RedirectView.as_view(url='swagger/')),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]