import os
from random import randint

from django.conf import settings
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from .models import *
from rest_framework import serializers
from base64 import b64encode, b64decode


DIFFICULTY_DICT = dict(PEREVAL_DIFFICULTIES)


# ====== User serialization =====


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Returns info about user."""

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


# ====== Image serialization =====


class Base64ImageField(serializers.ImageField):
    """Returns/accepts base64 encoded images instead of urls"""

    def to_representation(self, obj):
        """Grabs filepath, returns base64 encoded string"""
        full_path = os.path.join(settings.MEDIA_ROOT, obj.name)
        with open(full_path, 'rb') as picture:
            picture_content = picture.read()
        picture_content = b64encode(picture_content)
        return picture_content

    def to_internal_value(self, data):
        """It is necessary to overload this method in order for PerevalSerializer.create() method to work properly."""
        return data


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    """Lists images for pereval. In base64 encoding."""
    data = Base64ImageField(source='path')

    class Meta:
        model = Image
        fields = ['data', 'title']


# ====== Coordinates and pereval levels serialization =====


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    """Returns coordinates as a separate dict"""
    class Meta:
        model = Added
        fields = ['latitude', 'longitude', 'height']


class LevelChoiceField(serializers.CharField):
    """This returns/accepts labels("2-Б") instead of values (4)."""

    def __init__(self, **kwargs):  # regrettably, some hacks were... required
        kwargs['required'] = False
        kwargs['allow_null'] = True
        super().__init__(**kwargs)

    def to_representation(self, data):
        try:
            return DIFFICULTY_DICT[data]
        except KeyError:
            return None

    def to_internal_value(self, data):
        for key, value in DIFFICULTY_DICT.items():
            if value == data:
                return key
        if data is None or data == '':
            return None
        raise ValidationError(
            f'Выбрана несуществующая категория перевала. Возможные значения: {DIFFICULTY_DICT.values()}')


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    """Returns dificulty levels as a separate dict.
    Note: if level is unspecified, returns null
    """
    winter = LevelChoiceField(source='level_winter',)
    summer = LevelChoiceField(source='level_summer',)
    autumn = LevelChoiceField(source='level_autumn',)
    spring = LevelChoiceField(source='level_spring',)

    class Meta:
        model = Added
        fields = ['winter', 'summer', 'autumn', 'spring']


# ====== And, finally... =====


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    """Main serializer class. Returns/absorbs formatted info about pereval"""

    coords = CoordsSerializer(source='*')
    level = LevelSerializer(source='*')
    user = NonUniqueValidatingUserSerializer()
    images = ImagesSerializer(source='image_set', many=True)

    class Meta:
        model = Added
        fields = ['pk', 'status', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user',
                  'coords', 'level', 'images']

    def create(self, validated_data: dict):

        # ====== Step 1 - popping images and user data from validated data

        user_data = dict(validated_data.pop('user'))
        user_images = validated_data.pop('image_set')

        # ====== Step 2 - Creating or updating User

        email = user_data.pop('email')
        non_null_user_fields = {key: value for key, value in user_data.items() if value is not None and value != ''}
        user, was_created = User.objects.update_or_create(email=email, defaults=non_null_user_fields)

        # ====== Step 3 - Saving pereval to Added (without images)

        new_pereval = Added.objects.create(user=user, **validated_data)

        # ====== Step 4 - Saving images to storage and creating database entries
        # Note: due to the way the serializer is implemented, image contents are stored in 'path'. Confusing, I know=)
        # TODO this should ideally be modified to work with django storage api instead of naive python open()

        base_dir = os.path.join(settings.MEDIA_ROOT, PEREVAL_PHOTO_UPLOAD_DIR)

        for index, image in enumerate(user_images):
            file_name = f'pereval_{new_pereval.pk}_img_{index}_{randint(10000, 99999)}.jpg'
            full_path = os.path.join(base_dir, file_name)

            with open(full_path, 'wb') as picture:
                picture.write(b64decode(image["path"]))

            Image.objects.create(added=new_pereval, path=PEREVAL_PHOTO_UPLOAD_DIR + file_name, title=image['title'])

        return new_pereval
