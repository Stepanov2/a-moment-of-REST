from .models import *
from rest_framework import serializers


class DancerSerializer(serializers.HyperlinkedModelSerializer):
    num_groups = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Dancer
        fields = ['pk', 'name', 'born', 'dance_groups', 'age', 'num_groups']


    def get_num_groups(self, obj):
        return obj.dance_groups.count()


class DanceGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DanceGroup
        fields = ['pk', 'name', 'dancer_set']

