from .models import Tags, Blogs
from django.contrib import admin

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tags', 'date')

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'date', 'text', 'num_responses', 'num_claps', 'tags')