from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = ['data', 'title']

    def get_data(self, obj):
        """Returns Image contents in JSON format"""
        #todo
        return '<image will be here>'

class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    coords = serializers.SerializerMethodField(read_only=True)
    level = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']

    def get_coords(self, obj):
        # print(obj.level_autumn.__dict__)
        return {
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'height': obj.height,
        }

    def get_level(self, obj):
        return {}



# class DancerSerializer(serializers.HyperlinkedModelSerializer):
#     num_groups = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Dancer
#         fields = ['pk', 'name', 'born', 'dance_groups', 'age', 'num_groups']
#
#
#     def get_num_groups(self, obj):
#         return obj.dance_groups.count()
#
#
# class DanceGroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DanceGroup
#         fields = ['pk', 'name', 'dancer_set']

