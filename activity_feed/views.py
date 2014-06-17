# -*- coding: utf-8 -*-
"""
Django views.

"""
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render

from activity_feed import models


def activities(request, creator=None, target=None, page=1):
    """
    Activities administration page.

    """
    context = {}

    template = 'admin.html'
    list_template = 'activity_list.html'

    activities = models.Activity.objects.get_by(creator_id=creator,
                                                target_id=target)

    if request.is_ajax():  # render activity list
        template = list_template
        context = {'activities': activities}
    else:  # render full page
        activity_categories = models.Activity.CATEGORIES
        users = models.User.objects.select_subclasses()
        uri = _create_filter_uri(creator, target)

        context = {'activities': activities,
                   'activity_categories': activity_categories,
                   'activity_list_template': list_template,
                   'users': users,
                   'current_uri': uri}

    return render(request, template, context)


def create_activity(request):
    """
    Creates new activity.

    """
    if request.method == 'POST':
        creator = request.POST.get('creator')
        target = request.POST.get('target')
        category = request.POST.get('category')
        content = request.POST.get('content')

        activity = models.Activity.objects.create(creator_id=creator,
                                                  target_id=target,
                                                  category=category,
                                                  custom_content=content)

        if request.is_ajax():
            if activity:
                context = {'activities': [activity]}
                return render(request, 'activity_list.html', context)
            else:
                return ""

    return redirect('/')


def filter_activities(request):
    """
    Filter activities by creator and target user.

    Creators and targets are recognized by its id.

    """
    uri = '/'
    if request.method == 'GET':
        creator = request.GET.get('creator')
        creator = creator if creator != '' else None

        target = request.GET.get('target')
        target = target if target != '' else None

        uri = _create_filter_uri(creator, target)

    return redirect(uri)


def _create_filter_uri(creator_id, target_id):
    """
    Creates URI address to filter page.

    Attributes:
        creator_id (int or str or None): An ID of creator.
        target_id (int or str or None): An ID of target user.

    Returns:
        A string with address.

    """
    return reverse('activity_feed.views.activities',
                   kwargs={'creator': creator_id,
                           'target': target_id})
