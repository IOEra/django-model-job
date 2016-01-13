from django.contrib import admin

from .models import Job, Task, JobRule


class JobRuleInline(admin.TabularInline):
    model = JobRule


class TaskInline(admin.TabularInline):
    model = Task


class JobAdmin(admin.ModelAdmin):
    inlines = [
        JobRuleInline, TaskInline
    ]


admin.site.register(Job, JobAdmin)
