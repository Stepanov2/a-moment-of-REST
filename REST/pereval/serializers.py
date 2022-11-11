import os
from django.conf import settings

from .models import *
from rest_framework import serializers
from base64 import b64encode, b64decode


DIFFICULTY_DICT = dict(PEREVAL_DIFFICULTIES)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Returns info about user."""
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class Base64ImageField(serializers.ImageField):
    """Returns/accepts base64 encoded images instead of urls"""
    # TODO this should ideally be modified to work with django storage api instead of naive python open()
    def to_representation(self, obj):
        """Grabs filepath, returns base64 encoded string"""
        full_path = os.path.join(settings.MEDIA_ROOT, obj.name)
        with open(full_path, 'rb') as picture:
            picture_content = picture.read()
        picture_content = b64encode(picture_content)
        return picture_content

    def to_internal_value(self, data):
        """Grabs base64 encoded string, dumps it into file, creates filefield."""
        pass  # todo=)


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    """Lists images for pereval."""
    data = Base64ImageField(source='path')

    class Meta:
        model = Image
        fields = ['data', 'title']


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    """Returns coordinates as a separate dict"""
    class Meta:
        model = Added
        fields = ['latitude', 'longitude', 'height']


class LevelChoiceField(serializers.IntegerField):
    """This returns/accepts labels("2-Б") instead of values (4)."""

    def to_representation(self, data):
        try:
            return DIFFICULTY_DICT[data]
        except KeyError:
            return None

    def to_internal_value(self, data):
        for key, value in DIFFICULTY_DICT.items():
            if value == data:
                return key
        self.fail('Выбрана несуществующая категория перевала.', input=data)


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    """Returns dificulty levels as a separate dict.
    Note: if level is unspecified, returns null
    """
    winter = LevelChoiceField(source='level_winter')
    summer = LevelChoiceField(source='level_summer')
    autumn = LevelChoiceField(source='level_autumn')
    spring = LevelChoiceField(source='level_spring')

    class Meta:
        model = Added
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    """Main serializer class. Returns formatted info about pereval"""
    coords = CoordsSerializer(source='*')
    level = LevelSerializer(source='*')
    user = UserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']
