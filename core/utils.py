from django.core.cache import cache
from .models import SiteSettings


def get_site_settings():
    """
    Retrieve the singleton SiteSettings instance, using caching to minimize database hits.
    """
    settings = cache.get('site_settings')
    if not settings:
        settings = SiteSettings.load()
        cache.set('site_settings', settings, None)
    return settings
