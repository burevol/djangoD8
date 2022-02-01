from django.contrib import admin

from .models import Author, Category, Comment, Post


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'rating', 'type', 'date', 'author')
    list_filter = ('type', 'date', 'author')


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
