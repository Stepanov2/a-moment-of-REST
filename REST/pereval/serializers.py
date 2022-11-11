from .models import *
from rest_framework import serializers

DIFFICULTY_DICT = dict(PEREVAL_DIFFICULTIES)


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
    winter = LevelChoiceField(source='level_winter')
    summer = LevelChoiceField(source='level_summer')
    autumn = LevelChoiceField(source='level_autumn')
    spring = LevelChoiceField(source='level_spring')

    class Meta:
        model = Added
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    coords = CoordsSerializer(source='*')
    level = LevelSerializer(source='*')
    user = UserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']

