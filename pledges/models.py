from django.db import models
from better_profanity import profanity


class Pledge(models.Model):
    short_text = models.CharField(max_length=200)
    long_text = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_text


class Submission(models.Model):
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    consent_given = models.BooleanField(default=False)
    personal_pledge = models.TextField(blank=True, max_length=200)
    personal_pledge_censored = models.TextField(blank=True, editable=False)
    allow_display = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def save(self, *args, **kwargs):
        if self.personal_pledge:
            self.personal_pledge_censored = profanity.censor(self.personal_pledge)
        else:
            self.personal_pledge_censored = ''
        super().save(*args, **kwargs)
