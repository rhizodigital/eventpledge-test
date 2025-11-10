from django.db import models


class SingletonModel(models.Model):
    """
    An abstract base class for singleton models.
    Ensures that only one instance of the model exists.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1  # Always set the primary key to 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion of the singleton instance

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f'{self.__class__.__name__} Singleton Instance'
