from django.contrib import admin

from .models import Content
from .models import Category
from .models import Tag


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'title', 'category', 'created')
    list_display_links = ('title',)
    search_fields = ('title', 'category', 'created')
    list_filter = ('state', 'category', 'created', 'tags')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Content, ContentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
