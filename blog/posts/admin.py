from django.contrib import admin
from .models import Category, Topic, Post


# Kategorie
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
    ordering = ['name']  # sortowanie alfabetyczne


# Tematy
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['category']  # filtr kategorii
    search_fields = ['name']
    ordering = ['name']


# Posty
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'topic_with_category', 'created_by', 'created_at', 'updated_at']
    list_filter = ['topic__name', 'topic__category__name', 'created_by']
    search_fields = ['title', 'text']
    readonly_fields = ['created_at']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']

    @admin.display(description='Topic (Category)')
    def topic_with_category(self, obj):
        return f"{obj.topic.name} ({obj.topic.category.name})"

