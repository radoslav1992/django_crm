from django.contrib import admin
from .models import AIConversation, AIMessage, AISuggestion


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'user__email')
    ordering = ('-updated_at',)


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'content_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(AISuggestion)
class AISuggestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'suggestion_type', 'title', 'is_applied', 'is_dismissed', 'created_at')
    list_filter = ('suggestion_type', 'is_applied', 'is_dismissed', 'created_at')
    search_fields = ('title', 'content', 'user__email')
    ordering = ('-created_at',)

