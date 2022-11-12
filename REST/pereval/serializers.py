import os
from django.conf import settings
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from .models import *
from rest_framework import serializers
from base64 import b64encode, b64decode


DIFFICULTY_DICT = dict(PEREVAL_DIFFICULTIES)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Returns info about user."""
    # email = serializers.EmailField(validators=[])
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class NonUniqueValidatingUserSerializer(UserSerializer):
    """Since we "update_or_create" a User instance, when adding pereval, uniqueness check is not necessary.
    It is, however still very important to keep unique=True in user model, to prevent shenanigans. 
    This pops "UniqueValidator" but preserves all the other validators (MaxLength, Email, etc...).
    """

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

        for index, value in enumerate(self.fields['email'].validators):
            if isinstance(value, UniqueValidator):
                self.fields['email'].validators.pop(index)
                break


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
    """This returns/accepts labels("2-Б") instead of values (4).
    """

    def __init__(self, **kwargs):  # regrettably, some hacks were... required
        super().__init__(**kwargs)
        self.required = False

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
    winter = LevelChoiceField(source='level_winter', required=False)
    summer = LevelChoiceField(source='level_summer', required=False)
    autumn = LevelChoiceField(source='level_autumn', required=False)
    spring = LevelChoiceField(source='level_spring', required=False)

    class Meta:
        model = Added
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    """Main serializer class. Returns formatted info about pereval"""
    coords = CoordsSerializer(source='*')
    level = LevelSerializer(source='*')
    user = NonUniqueValidatingUserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']

    def create(self, validated_data:dict):
        print(validated_data)
        # print(self.__dict__)

        # ====== Step 1 - popping images and user data from validated data

        user_data = dict(validated_data.pop('user'))
        user_images = validated_data.pop('image_set')
        # coordinates = validated_data.pop('coords')
        # validated_data = {**validated_data, **coordinates}


        # ====== Step 2 - Creating or updating User

        email = user_data.pop('email')
        non_null_user_fields = {key: value for key, value in user_data.items() if value is not None and value != ''}
        user, was_created = User.objects.update_or_create(email=email,
                                             defaults=non_null_user_fields)  # debug

        # if User.objects.filter(email=validated_data['email'])[0].exists():
        #     user = User.objects.get(email=validated_data['email'])

        # ====== Step 3 - Saving pereval to Added (without images)

        new_pereval = Added.objects.create(user=user, **validated_data)

        # ====== Step 4 - Saving images to pereval

        pass

        return new_pereval
