from django.contrib import admin

from .models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    empty_value_display = 'EMPTY!'


admin.site.register(Group, GroupAdmin)
