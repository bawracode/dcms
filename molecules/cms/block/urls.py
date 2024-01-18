from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:slug_url>/', views.index, name='dynamic_template_view'),
]