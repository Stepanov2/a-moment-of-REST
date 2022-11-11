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
        return f'<image "{obj.title}" will be here>'


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Added
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Added
        fields = ['level_winter', 'level_summer', 'level_autumn', 'level_spring']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    coords = CoordsSerializer(source='*')
    level = LevelSerializer(source='*')
    user = UserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']

