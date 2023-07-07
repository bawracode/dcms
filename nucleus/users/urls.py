from django.urls import path, include
from . import views

urlpatterns = [
    path('save_prefrences/', views.save_prefrences_user, name='save_prefrences'),
]
