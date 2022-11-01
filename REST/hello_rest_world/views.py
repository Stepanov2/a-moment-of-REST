from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Dancer, DanceGroup, DanceGroupDancers
from .serializers import *
# Create your views here.
class DancerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dancer.objects.all().order_by('name')
    serializer_class = DancerSerializer



class DanceGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = DanceGroup.objects.all()
    serializer_class = DanceGroupSerializer
