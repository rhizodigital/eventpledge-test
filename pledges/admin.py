from django.contrib import admin
from .models import Pledge, Submission
from django.db.models import Count

admin.site.site_header = 'Event Pledge Administration'
admin.site.site_title = 'Event Pledge Admin'
admin.site.index_title = 'Welcome to Event Pledge Admin'


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'is_active', 'submission_count')
    list_filter = ('is_active',)
    search_fields = ('short_text', 'long_text')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(_submission_count=Count('submission'))
        return qs

    def submission_count(self, obj):
        return getattr(obj, '_submission_count', 0)

    submission_count.admin_order_field = '_submission_count'
    submission_count.short_description = 'Number of Submissions'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'pledge', 'consent_given', 'timestamp')
    list_filter = ('consent_given', 'pledge')
    search_fields = ('first_name', 'last_name', 'personal_pledge')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'personal_pledge_censored')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'pledge',
                    ('first_name', 'last_name'),
                    'consent_given',
                    'allow_display',
                    'personal_pledge',
                    'personal_pledge_censored',
                    'timestamp',
                )
            },
        ),
    )
