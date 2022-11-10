from django.contrib import admin
from .models import User, Added, Image
# Register your models here.


class AddedPhotoInline(admin.TabularInline):
    model = Image
    extra = 3


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('pk', 'email', 'fam', 'name', 'otc')
    search_fields = ('email', 'fam', 'name')
    list_display_links = ('email',)


@admin.register(Added)
class AddedAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'status', )
    search_fields = ('user_email', 'title')
    inlines = [AddedPhotoInline,]
    ordering = ('status', '-pk')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)
    search_fields = ('title',)
    list_display_links = ('title',)



