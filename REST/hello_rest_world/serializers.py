from .models import *
from rest_framework import serializers


class DancerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dancer
        fields = ['pk', 'name', 'born', 'dance_groups']


class DanceGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DanceGroup
        fields = ['pk', 'name', 'dancer_set']

