from django.shortcuts import render, redirect
from .models import Pledge, Submission
from .forms import SubmissionForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

testing_form_submission = True


def index(request):
    if request.session.get('has_submitted') and not testing_form_submission:
        return render(request, 'pledges/thank_you.html')
    form = SubmissionForm()
    form.fields['pledge'].queryset = Pledge.objects.filter(is_active=True)
    return render(request, 'pledges/form.html', {'form': form})


def _broadcast_counts():
    layer = get_channel_layer()
    data = {
        p.short_text: Submission.objects.filter(pledge=p).count()
        for p in Pledge.objects.filter(is_active=True)
    }
    async_to_sync(layer.group_send)(
        'live_counts',
        {
            'type': 'counts.update',
            'data': data,
        },
    )


def submit_pledge(request):
    if request.session.get('has_submitted') and not testing_form_submission:
        return render(request, 'pledges/thank_you.html')

    form = SubmissionForm(request.POST or None)
    form.fields['pledge'].queryset = Pledge.objects.filter(is_active=True)
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['has_submitted'] = True
        request.session.modified = True
        _broadcast_counts()
        return redirect('thank_you')

    return render(request, 'pledges/form.html', {'form': form})


def thank_you(request):
    return render(request, 'pledges/thank_you.html')


def live_visualisation(request, chart_type='barchart'):
    pledges = Pledge.objects.filter(is_active=True)
    counts = {p.short_text: Submission.objects.filter(pledge=p).count() for p in pledges}

    if chart_type == 'barchart':
        template = 'pledges/live_barchart.html'

    return render(request, template, {'counts': counts})
