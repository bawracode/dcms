from django.urls import path,include
from . import views
from .views import *



urlpatterns = [
path('language-selection/', language_selection_view, name='language_selection'),
    path('upload-po/', po_file_view, name='upload_po_file'),
]
