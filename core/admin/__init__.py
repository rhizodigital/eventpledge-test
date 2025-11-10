from django.contrib import admin
from .base import SingletonModelAdmin
from core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': ('site_name',),
            },
        ),
        (
            'Submisson form settings',
            {
                'classes': ('collapse',),
                'fields': (
                    'submission_form_heading',
                    'submission_form_subheading',
                    'consent_text',
                    'privacy_policy',
                ),
            },
        ),
        (
            'Visualisation settings',
            {
                'classes': ('collapse',),
                'fields': (
                    'visualisation_font_factor',
                    'visualisation_hero_heading',
                    'visualisation_hero_subheading',
                ),
            },
        ),
    )
