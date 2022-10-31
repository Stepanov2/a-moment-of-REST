from django.contrib import admin
from .models import Dancer, DanceGroup, DanceGroupDancers
# Register your models here.


class DancerDanceGroupInline(admin.TabularInline):
    model = Dancer.dance_groups.through
    extra = 3


class DanceGroupDancerInline(admin.TabularInline):
    model = DanceGroup.dancer_set.through
    extra = 3


@admin.register(Dancer)
class SiteUserAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('pk', 'name',
                    'born')
    search_fields = ('name', 'born')
    list_display_links = ('name',)
    inlines = (DancerDanceGroupInline,)


@admin.register(DanceGroup)
class SiteUserAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('pk', 'name',
                    'established')
    search_fields = ('name', 'established')
    list_display_links = ('name',)
    inlines = (DanceGroupDancerInline,)




