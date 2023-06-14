from django.urls import path, include
from . import views

urlpatterns = [
    path('render/<str:template_name>/', views.dynamic_template_view, name='dynamic_template_view'),
    path("index/", views.index, name="index")
]