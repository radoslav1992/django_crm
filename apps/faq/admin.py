from django.contrib import admin
from .models import FAQCategory, FAQItem


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'item_count']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def item_count(self, obj):
        return obj.items.filter(is_active=True).count()
    item_count.short_description = 'Брой въпроси'


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_featured', 'is_active', 'views_count']
    list_editable = ['order', 'is_featured', 'is_active']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['question', 'answer', 'question_en', 'answer_en']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основна информация', {
            'fields': ('category', 'order', 'is_active', 'is_featured')
        }),
        ('Съдържание (Български)', {
            'fields': ('question', 'answer')
        }),
        ('Съдържание (Английски)', {
            'fields': ('question_en', 'answer_en'),
            'classes': ('collapse',)
        }),
        ('Допълнителни настройки', {
            'fields': ('guide_file', 'views_count', 'created_at', 'updated_at')
        }),
    )

