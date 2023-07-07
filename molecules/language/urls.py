from django.urls import path,include
from . import views
from .views import language_selection_view



urlpatterns = [
path('language-selection/', language_selection_view, name='language_selection'),
]
