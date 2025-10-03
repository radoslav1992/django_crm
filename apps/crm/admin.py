from django.contrib import admin
from .models import Company, Contact, Pipeline, Stage, Deal, Task, Activity, CustomField


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'city', 'country', 'owner', 'created_at')
    list_filter = ('industry', 'country', 'created_at')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'company', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('name',)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'pipeline', 'probability', 'order')
    list_filter = ('pipeline',)
    ordering = ('pipeline', 'order')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'currency', 'status', 'stage', 'owner', 'created_at')
    list_filter = ('status', 'pipeline', 'stage', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'priority', 'due_date', 'completed', 'assigned_to', 'created_at')
    list_filter = ('task_type', 'priority', 'completed', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('completed', '-due_date', '-created_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'contact', 'company', 'deal', 'owner', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'entity_type', 'field_type', 'is_required', 'owner', 'created_at')
    list_filter = ('entity_type', 'field_type', 'is_required')
    ordering = ('entity_type', 'order')

