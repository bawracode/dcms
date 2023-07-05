from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import UserSerializer
from .serializers import PostSerializer
from rest_framework.permissions import *
from rest_framework.response import Response
import logging

logger = logging.getLogger('api_calls')

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get','post']
    def get(self, request):
        # Your view logic here
        logger.info("Sample API call: GET request")
        return Response({'message': 'API call successful'})
    def get_queryset(self):
        queryset = User.objects.all()
        print(self.request.path.split('/')[-3:-1],"self.request")
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get',]
    def get(self, request):
        # Your view logic here
        logger.info("Sample API call: GET request")
        return Response({'message': 'API call successful'})
    def get_queryset(self):
        queryset = Post.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset
