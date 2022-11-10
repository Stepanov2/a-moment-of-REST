from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import *


class PerevalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or add perevals
    """
    queryset = Added.objects.all().order_by('status', '-add_time')
    serializer_class = PerevalSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    Returns image(s) for pereval.
    """
    queryset = Image.objects.all()
    serializer_class = ImagesSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Returns image(s) for pereval.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
