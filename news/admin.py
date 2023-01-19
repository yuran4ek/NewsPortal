from django.contrib import admin
from .models import Author, Post, Category, Comment, SubscribeCategories


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubscribeCategories)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categories', 'get_subscribers')


admin.site.register(Category, CategoryAdmin, )
