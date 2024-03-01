from django.contrib import admin
from .models import Profile, TestName


@admin.register(TestName)
class TestNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
