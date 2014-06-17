# -*- coding: utf-8 -*-
"""
Django models.

"""
from __future__ import unicode_literals

from django.core import exceptions
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from activity_feed.monkeypatches import InheritanceManager


class User(models.Model):
    """
    Generic user model.

    """
    objects = InheritanceManager()


@python_2_unicode_compatible
class Employee(User):
    """
    Employee model.

    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


@python_2_unicode_compatible
class CoffeeCompany(User):
    """
    Coffee company model.

    """
    full_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'coffee companies'

    def __str__(self):
        return self.full_name


class ActivityManager(models.Manager):
    def all(self):
        """
        Returns a list of all model instances sorted by create date.

        Returns:
            A QuerySet iterable object.

        """
        return super(ActivityManager, self).all().order_by('-created')

    def create(self, creator_id, target_id, category=None, custom_content=None):
        """
        Creates instance of Activity class.

        Attributes:
            creator_id (int or str): An ID of creator.
            target_id (int or str): An ID of target user.
            category (str or None): A category of activity.
            custom_content (str or None): A custom content of activity.

        Returns:
            An Activity class instance.

        """
        content = ""

        if category:  # content from category, formatted for website
            content = "{} {} {}".format(
                User.objects.get(id=creator_id),
                category,
                User.objects.get(id=target_id))
        elif custom_content:  # custom content
            content = custom_content

        return super(ActivityManager, self).create(creator_id=creator_id,
                                                   target_id=target_id,
                                                   content=content)

    def get_by(self, creator_id, target_id):
        """
        Returns a list of activities filtered by creator and target.

        Attributes:
            creator_id (int or str or None): An ID of creator.
            target_id (int or str or None): An ID of target user.

        Returns:
            A QuerySet iterable object.

        """
        activities = super(ActivityManager, self).all()
        if creator_id:
            activities = activities.filter(creator__id=creator_id)
        if target_id:
            activities = activities.filter(target__id=target_id)

        return activities


@python_2_unicode_compatible
class Activity(models.Model):
    """
    Activity model.

    """
    CATEGORIES = ({'id': 'invitation', 'content': 'invited'},
                  {'id': 'drinking', 'content': 'drinked coffee from'},
                  {'id': 'delivering', 'content': 'delivered product to'}, )

    creator = models.ForeignKey(User, related_name='creators')
    target = models.ForeignKey(User, related_name='targets')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = ActivityManager()

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.content

    def clean(self, *args, **kwargs):
        if not self.content:  # incorrect activity, don't save
            raise exceptions.ValidationError('Activities must have a content.')

    def save(self, *args, **kwargs):
        try:
            self.clean()
            super(Activity, self).save(*args, **kwargs)
        except exceptions.ValidationError:
            pass
