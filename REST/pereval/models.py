from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    """A dirty little hack to allow PyCharm community edition (and, possibly other IDEs) to correctly resolve
    .objects for models. # God bless stack overflow!
    """

    objects = models.Manager()

    class Meta:
        abstract = True


PEREVAL_DIFFICULTIES = [
    (1, '1-А'),
    (2, '1-Б'),
    (3, '2-А'),
    (4, '2-Б'),
    (5, '3-А'),
    (6, '3-Б'),
]


class PerevalCategoryField(models.PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = PEREVAL_DIFFICULTIES
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


def validate_coordinates(value: float):
    if not (-90 <= value <= 90):
        raise ValidationError(f'одна из координат перевала выходит за границы допустимых значений. {value} ∉ [-90,90] ')


def validate_height(value:int):
    if not (0 <= value <= 8850):
        raise ValidationError(f'Неверная высота. {value} ∉ [0,8850] ')


class CoordinateField(models.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['validators'] = [validate_coordinates]
        super().__init__(*args, **kwargs)


class HeightField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['validators'] = [validate_height]
        super().__init__(*args, **kwargs)


class User(BaseModel):
    """Почта пользователя перевала.
    Поля - pk, email"""
    email = models.EmailField(unique=True, blank=False)
    fam = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    otc = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc} <{self.email}>'


class Added(BaseModel):
    """Обзор перевала, добавленный пользователем"""
    beauty_title = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100, null=True, blank=True)
    connect = models.CharField(max_length=200, null=True, blank=True)

    level_summer = PerevalCategoryField()
    level_autumn = PerevalCategoryField()
    level_winter = PerevalCategoryField()
    level_spring = PerevalCategoryField()

    latitude = CoordinateField()
    longitude = CoordinateField()
    altitude = HeightField()

    class Meta:
        pass

    def __str__(self):
        return self.name
    pass


class Image(BaseModel):
    """Фото, загруженные пользователями"""
    added = models.ForeignKey(Added, on_delete=models.CASCADE)
    path = models.ImageField(upload_to='pereval_photo/',)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['added', 'title']

    def __str__(self):
        return self.title

