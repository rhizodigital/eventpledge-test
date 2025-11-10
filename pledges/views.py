from django.db.models import Count
from django.db import transaction
from django.shortcuts import render, redirect
from .models import Pledge, Submission
from .forms import SubmissionForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.site_settings_accessor import site_setting
from core.utils import get_site_settings


def _broadcast_live():
    layer = get_channel_layer()
    pledges_with_counts = Pledge.objects.filter(is_active=True).annotate(
        sub_count=Count('submission')
    )

    # Format the data into the dictionary {pledge_name: count}
    count_data = {p.short_text: p.sub_count for p in pledges_with_counts}

    latest_pledges_qs = (
        Submission.objects.filter(allow_display=True, personal_pledge_censored__isnull=False)
        .exclude(personal_pledge_censored='')
        .order_by('-timestamp')[:5]
    )

    pledge_feed = [
        {
            'first_name': s.first_name,
            'last_name': s.last_name,
            'personal_pledge_censored': s.personal_pledge_censored,
            'timestamp': s.timestamp.isoformat(),
        }
        for s in latest_pledges_qs
    ]

    async_to_sync(layer.group_send)(
        'live_feed',
        {
            'type': 'counts.update',
            'data': {
                'counts': count_data,
                'pledge_feed': pledge_feed,
            },
        },
    )


def submit_pledge(request):
    if request.session.get('has_submitted') and not site_setting('test_mode', False):
        return render(request, 'pledges/thank_you.html')

    form = SubmissionForm(request.POST or None)
    form.fields['pledge'].queryset = Pledge.objects.filter(is_active=True)
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['has_submitted'] = True
        request.session.modified = True

        transaction.on_commit(_broadcast_live)
        return redirect('thank_you')

    return render(request, 'pledges/form.html', {'form': form})


def thank_you(request):
    site_settings = get_site_settings()
    return render(request, 'pledges/thank_you.html', {'site_settings': site_settings})


def live_visualisation(request, chart_type='barchart'):
    pledges = Pledge.objects.filter(is_active=True)
    counts = {p.short_text: Submission.objects.filter(pledge=p).count() for p in pledges}

    if chart_type == 'barchart':
        template = 'pledges/live_barchart.html'

    latest_pledges = (
        Submission.objects.filter(allow_display=True, personal_pledge_censored__isnull=False)
        .exclude(personal_pledge_censored='')
        .order_by('-timestamp')[:5]
    )

    pledges_feed = [
        {
            'first_name': s.first_name,
            'last_name': s.last_name,
            'personal_pledge_censored': s.personal_pledge_censored,
            'timestamp': s.timestamp.isoformat(),
        }
        for s in latest_pledges
    ]

    site_settings = get_site_settings()

    return render(
        request,
        template,
        {
            'counts': counts,
            'latest_pledges': latest_pledges,
            'pledge_feed': pledges_feed,
            'site_settings': site_settings,
        },
    )
