from django.db import models
from core.models.base import SingletonModel
from django_prose_editor.fields import ProseEditorField
from core import settings_defaults as defaults
from django.core.validators import MinValueValidator, MaxValueValidator


class SiteSettings(SingletonModel):
    """
    A singleton model to store site-wide settings.
    """

    site_name = models.CharField(max_length=255, default=defaults.SITE_NAME)
    test_mode = models.BooleanField(default=defaults.TEST_MODE)
    submission_form_heading = models.CharField(
        max_length=255, blank=True, default=defaults.SUBMISSION_FORM_HEADING
    )
    submission_form_subheading = models.TextField(
        blank=True, default=defaults.SUBMISSION_FORM_SUBHEADING
    )
    thank_you_page_heading = models.CharField(
        max_length=70, blank=True, default=defaults.THANK_YOU_PAGE_HEADING
    )
    thank_you_page_subheading = models.TextField(
        blank=True, default=defaults.THANK_YOU_PAGE_SUBHEADING
    )
    consent_text = models.TextField(blank=True, default=defaults.CONSENT_TEXT)
    privacy_policy = ProseEditorField(
        extensions={
            # Core text formatting
            'Bold': True,
            'Italic': True,
            'Strike': True,
            'Underline': True,
            'HardBreak': True,
            # Structure
            'Heading': {
                'levels': [1, 2, 3]  # Only allow h1, h2, h3
            },
            'BulletList': True,
            'OrderedList': True,
            'ListItem': True,  # Used by BulletList and OrderedList
            'Blockquote': True,
            # Advanced extensions
            'Link': {
                'enableTarget': True,  # Enable "open in new window"
                'protocols': ['http', 'https', 'mailto'],  # Limit protocols
            },
            'Table': True,
            'TableRow': True,
            'TableHeader': True,
            'TableCell': True,
            # Editor capabilities
            'History': True,  # Enables undo/redo
            'HTML': True,  # Allows HTML view
            'Typographic': True,  # Enables typographic chars
        },
        sanitize=True,
        blank=True,
    )

    visualisation_font_factor = models.IntegerField(
        default=100,
        help_text='A percentage factor to scale the base font size used in visualisations. '
        'E.g., 100% is normal size, 80% is smaller, 120% is larger.',
        validators=[MinValueValidator(80), MaxValueValidator(120)],
    )

    visualisation_hero_heading = models.CharField(
        max_length=255,
        blank=True,
        default=defaults.VISUALISATION_FONT_HERO_HEADING,
    )
    visualisation_hero_subheading = models.TextField(
        blank=True,
        default=defaults.VISUALISATION_FONT_HERO_SUBHEADING,
    )

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'
