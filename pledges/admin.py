from django.contrib import admin
from .models import Pledge, Submission
from django.db.models import Count
from django.http import HttpResponse
import csv

admin.site.site_header = 'Event Pledge Administration'
admin.site.site_title = 'Event Pledge Admin'
admin.site.index_title = 'Welcome to Event Pledge Admin'


def export_pledge_counts_as_csv(modeladmin, request, queryset):
    """
    A view function that streams a CSV file
    of the selected pledges and their submission counts.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pledge_counts.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Pledge (Short Text)', 'Is Active', 'Submission Count'])

    # Write data rows
    # The queryset is already annotated by the PledgeAdmin.get_queryset method
    for pledge in queryset:
        writer.writerow(
            [
                pledge.short_text,
                pledge.is_active,
                getattr(pledge, '_submission_count', 0),  # Use the annotated count
            ]
        )

    return response


export_pledge_counts_as_csv.short_description = 'Export Selected Pledge Counts as CSV'


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'is_active', 'submission_count')
    list_filter = ('is_active',)
    search_fields = ('short_text', 'long_text')

    actions = [export_pledge_counts_as_csv]  # Add the new action here

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(_submission_count=Count('submission'))
        return qs

    def submission_count(self, obj):
        return getattr(obj, '_submission_count', 0)

    submission_count.admin_order_field = '_submission_count'
    submission_count.short_description = 'Number of Submissions'


def export_as_csv(modeladmin, request, queryset):
    """
    A view function that streams a CSV file
    of the selected submissions.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="submissions.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(
        [
            'First Name',
            'Last Name',
            'Pledge',
            'Personal Pledge',
            'Timestamp',
            'Consent Given',
            'Allow Display',
        ]
    )

    # Write data rows
    for submission in queryset.values_list(
        'first_name',
        'last_name',
        'pledge__short_text',  # Get the pledge's text
        'personal_pledge',
        'timestamp',
        'consent_given',
        'allow_display',
    ):
        writer.writerow(submission)

    return response


export_as_csv.short_description = 'Export Selected Submissions as CSV'


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
    actions = [export_as_csv]
