from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import routers
from molecules.api.views import *
from molecules.api.models import SystemConfig


routers = routers.DefaultRouter()
routers.register(r'users', UserViewSet,basename="create-post")
routers.register(r'posts', PostViewSet,basename="create-post")

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="A simple Blog API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),


)


urlpatterns = [
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
 path("", include(routers.urls)),
 path('toggle_ajax/', toggle_switch_ajax, name='toggle_switch_ajax'),
]
