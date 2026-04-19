from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified',  'is_active')
    search_fields = ('email',)
    list_filter = ('is_verified',  'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', )
    search_fields = ('full_name', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')
    search_fields = ('title',)
    list_filter = ('author', 'category')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating')
    search_fields = ('book', 'user')


