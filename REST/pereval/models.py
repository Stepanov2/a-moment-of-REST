from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


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

POSSIBLE_PEREVAL_STATUSES = [
    ('new', 'Загружено пользователем'),
    ('pending', 'Взято в проверку'),
    ('accepted', 'Принято'),
    ('rejected', 'Отклонено'),
]

class PerevalCategoryField(models.PositiveSmallIntegerField):
    """Поле выбора сложности перевала."""
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = PEREVAL_DIFFICULTIES
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


def validate_coordinates(value: float):
    """Убеждается, что мы на земле)"""
    if not (-90 <= value <= 90):
        raise ValidationError(f'одна из координат перевала выходит за границы допустимых значений. {value} ∉ [-90,90] ')


def validate_height(value: int):
    """Убеждается, что мы не выше Эвереста и не под водой) """
    if not (0 <= value <= 8850):
        raise ValidationError(f'Неверная высота. {value} ∉ [0,8850] ')


class CoordinateField(models.FloatField):
    """Поле широты/долготы"""
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['validators'] = [validate_coordinates]
        super().__init__(*args, **kwargs)


class HeightField(models.PositiveIntegerField):
    """Поле высоты."""
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['validators'] = [validate_height]
        super().__init__(*args, **kwargs)


class User(BaseModel):
    """Почта и прочие данные пользователя
    Поля - pk, email, fam, name, otc, phone"""
    email = models.EmailField(unique=True, blank=False)
    fam = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    otc = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        ordering = ['email']

    def __str__(self):
        fam = self.fam or ''
        name = self.name or ''
        otc = self.otc or ''
        full_name = ' '.join([fam, name, otc])
        return f'{full_name} <{self.email}>'


class Added(BaseModel):
    """Обзор перевала, добавленный пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100, null=True, blank=True)
    connect = models.CharField(max_length=200, null=True, blank=True)

    add_time = models.DateTimeField(null=True, auto_now_add=True)

    level_summer = PerevalCategoryField(null=True, blank=True)
    level_autumn = PerevalCategoryField(null=True, blank=True)
    level_winter = PerevalCategoryField(null=True, blank=True)
    level_spring = PerevalCategoryField(null=True, blank=True)

    latitude = CoordinateField()
    longitude = CoordinateField()
    height = HeightField()

    status = models.CharField(max_length=15, choices=POSSIBLE_PEREVAL_STATUSES, default='new')

    class Meta:
        ordering = ['add_time']

    def __str__(self):
        return f'{self.beauty_title} {self.title} ({self.other_titles})'
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

