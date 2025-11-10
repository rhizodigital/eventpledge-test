from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
import re
from .models import Submission

TAG_RE = re.compile(r'<[^>]+>')


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'first_name',
            'last_name',
            'pledge',
            'personal_pledge',
            'allow_display',
            'consent_given',
        ]
        labels = {
            'personal_pledge': 'Write your own pledge',
            'first_name': 'Your first name',
            'last_name': 'Your last name',
            'consent_given': 'Your permission',
            'pledge': 'Which pledge resonates with you?',
            'allow_display': 'I’m happy for my pledge to be shown on the event screen',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
            'last_name': forms.TextInput(),
            'pledge': forms.RadioSelect(),
            'personal_pledge': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        if TAG_RE.search(first_name):
            raise ValidationError(
                'Please don’t include HTML or special characters in your first name.'
            )
        if len(first_name.strip()) > 70:
            raise ValidationError('Your first name can’t be longer than 70 characters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        if TAG_RE.search(last_name):
            raise ValidationError(
                'Please don’t include HTML or special characters in your last name.'
            )
        if len(last_name.strip()) > 70:
            raise ValidationError('Your last name can’t be longer than 70 characters.')
        return last_name

    def clean_personal_pledge(self):
        personal_pledge = self.cleaned_data.get('personal_pledge', '')
        if TAG_RE.search(personal_pledge):
            raise ValidationError(
                'Please don’t include HTML or special characters in your personal pledge.'
            )
        if len(personal_pledge.strip()) > 360:
            raise ValidationError('Your personal pledge can’t be longer than 360 characters.')
        return personal_pledge

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pledge'].choices = [
            (p.id, f'<strong>{p.short_text}</strong> {p.long_text}')
            for p in self.fields['pledge'].queryset
        ]

        self.fields['consent_given'].required = True
        self.fields['consent_given'].error_messages = {
            'required': 'Please confirm you’re happy for us to use your information before submitting your pledge.'
        }
