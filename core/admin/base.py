from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


class SingletonModelAdmin(admin.ModelAdmin):
    """
    An abstract admin class for singleton models.
    Redirects to the singleton instance change page.
    """

    def has_add_permission(self, request):
        # Prevent adding new instances
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # Redirect to the singleton instance change page
        singleton_instance = self.model.load()
        return HttpResponseRedirect(
            reverse(
                f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
                args=(singleton_instance.pk,),
            )
        )

    def has_delete_permission(self, request, obj=None):
        return False
