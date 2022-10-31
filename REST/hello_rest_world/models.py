from datetime import datetime
from datetime import date

from django.db import models

# Create your models here.
from django.utils import timezone


class BaseModel(models.Model):
    """A dirty little hack to allow PyCharm community edition (and, possibly other IDEs) to correctly resolve
    .objects for models. # God bless stack overflow!
    """

    objects = models.Manager()

    class Meta:
        abstract = True


class DanceGroup(BaseModel):
    name = models.CharField(max_length=120)
    established = models.DateField(null=True)

    def __str__(self):
        return self.name


class Dancer(BaseModel):
    name = models.CharField(max_length=120)
    born = models.DateField(null=True)
    dance_groups = models.ManyToManyField(DanceGroup, through='DanceGroupDancers')

    def __str__(self):
        return self.name

    @property
    def age(self):
        if self.born is not None:
            today = date.today()
            return today.year - self.born.year - ((today.month, today.day) < (self.born.month, self.born.day))


class DanceGroupDancers(BaseModel):
    dancer = models.ForeignKey(Dancer, on_delete=models.CASCADE)
    dance_group = models.ForeignKey(DanceGroup, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['dancer', 'dance_group']
        ordering = ['dance_group', 'dancer_name']


