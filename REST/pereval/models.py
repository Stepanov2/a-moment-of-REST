from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    """A dirty little hack to allow PyCharm community edition (and, possibly other IDEs) to correctly resolve
    .objects for models. # God bless stack overflow!
    """

    objects = models.Manager()

    class Meta:
        abstract = True


# ====== Константы =====


PEREVAL_DIFFICULTIES = [
    (1, '1-А'),
    (2, '1-Б'),
    (3, '2-А'),
    (4, '2-Б'),
    (5, '3-А'),
    (6, '3-Б'),
]

PEREVAL_POSSIBLE_STATUSES = [
    ('new', 'Загружено пользователем'),
    ('pending', 'Взято в проверку'),
    ('accepted', 'Принято'),
    ('rejected', 'Отклонено'),
]

PEREVAL_PHOTO_UPLOAD_DIR = 'pereval_photo/'


# ====== Поля и валидаторы =====


class PerevalCategoryField(models.PositiveSmallIntegerField):
    """Поле выбора сложности перевала."""
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = PEREVAL_DIFFICULTIES
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


def validate_coordinates(value: float):
    """Убеждается, что нам дали корректную полярную координату)"""
    if not (-90 <= value <= 90):
        raise ValidationError(f'одна из координат перевала выходит за границы допустимых значений. {value} ∉ [-90,90] ')


def validate_height(value: int):
    """Убеждается, что мы не выше Эвереста и не под водой) """
    if not (0 <= value <= 8850):
        raise ValidationError(f'Неверная высота. {value} ∉ [0,8850] ')


class CoordinateField(models.FloatField):
    """Поле широты/долготы"""
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_coordinates]
        super().__init__(*args, **kwargs)


class HeightField(models.PositiveIntegerField):
    """Поле высоты."""
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_height]
        super().__init__(*args, **kwargs)


# ====== Модели =====


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
        """Иванов Иван Иванович <hi@example.com>"""
        fam = self.fam or ''
        name = self.name or ''
        otc = self.otc or ''
        full_name = ' '.join([fam, name, otc])
        return f'{full_name} <{self.email}>'


class Added(BaseModel):
    """Обзор перевала, добавленный пользователем
    Поля - pk, user, beauty_title, title, other_titles, connect,
    add_time, level_summer/autumn/winter/spring, latitude, longiude, height, status"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100, null=True, blank=True)
    connect = models.CharField(max_length=200, null=True, blank=True)

    add_time = models.DateTimeField()

    level_summer = PerevalCategoryField()
    level_autumn = PerevalCategoryField()
    level_winter = PerevalCategoryField()
    level_spring = PerevalCategoryField()

    latitude = CoordinateField()
    longitude = CoordinateField()
    height = HeightField()

    status = models.CharField(max_length=15, choices=PEREVAL_POSSIBLE_STATUSES, default='new')

    class Meta:
        ordering = ['add_time']

    def __str__(self):
        """пер. Кривой (Прямой)"""
        beauty_title = self.beauty_title or ''
        other_titles = f'({self.other_titles})' if self.other_titles else ''
        return f'{beauty_title} {self.title} {other_titles}'.strip()
    pass


class Image(BaseModel):
    """Фото, загруженные пользователями"""
    added = models.ForeignKey(Added, on_delete=models.CASCADE)
    path = models.ImageField(upload_to=PEREVAL_PHOTO_UPLOAD_DIR, )
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['added', 'title']

    def __str__(self):
        return self.title
