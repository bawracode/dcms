from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.index, name='index'), 
    path('return_sub_section/', views.return_sub_section, name='return_sub_section'),
    path('return_option/',view=views.return_option,name='return_option'),
    path('save_change_value/',view=views.save_value,name='save_change_value')
]
