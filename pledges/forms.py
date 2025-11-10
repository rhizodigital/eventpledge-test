from django import forms
from .models import Submission


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
            'allow_display': 'I’m happy for my name and pledge to be shown on the event screen.',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
            'last_name': forms.TextInput(),
            'pledge': forms.RadioSelect(),
            'personal_pledge': forms.Textarea(attrs={'rows': 3}),
        }

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
