from core.utils import get_site_settings


def site_setting(setting_name, default=None):
    settings = get_site_settings()
    if setting_name:
        return getattr(settings, setting_name, default)
    return settings
