from django.contrib import admin
from .models import Post, Response, OneTimeCode

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'is_accepted', 'created_at')
    list_filter = ('is_accepted',)

@admin.register(OneTimeCode)
class OneTimeCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
