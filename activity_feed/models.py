#-*- coding: utf-8 -*-
"""
Django models.

"""
from __future__ import unicode_literals

from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from activity_feed.decorators import cached
from activity_feed.monkeypatches import InheritanceManager


class UserManager(models.Manager):
    def get(self):
        return self.select_subclasses()


class User(models.Model):
    """
    Generic user model.

    """
    objects = InheritanceManager()

    @classmethod
    @cached('all_users')
    def get_all(cls):
        """
        Returns a list of all inherited models.

        Returns:
            A QuerySet iterable object.

        """
        return cls.objects.select_subclasses()

    @classmethod
    def get_by_id(cls, user_id):
        """
        Returns a User object with specified id.

        Attributes:
            user_id (int or str): An ID of user.

        Returns:
            A User object.

        """
        return cls.objects.get(id=user_id)


@python_2_unicode_compatible
class Employee(User):
    """
    Employee model.

    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    @cached('all_employees')
    def get_all(cls):
        """
        Returns a list of all model instances.

        Returns:
            A QuerySet iterable object.

        """
        return cls.objects.all()


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

    @classmethod
    @cached('all_coffee_companies')
    def get_all(cls):
        """
        Returns a list of all model instances.

        Returns:
            A QuerySet iterable object.

        """
        return cls.objects.all()


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
    content = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.content

    @classmethod
    def create(cls, creator_id, target_id, category=None, custom_content=None):
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
            content = "{} {} {}".format(User.get_by_id(creator_id),
                                        category,
                                        User.get_by_id(target_id))
        elif custom_content:  # custom content
            content = custom_content

        return cls(creator_id=creator_id,
                   target_id=target_id,
                   content=content)

    @classmethod
    @cached('all_activities')
    def get_all(cls):
        """
        Returns a list of all model instances sorted by create date.

        Returns:
            A QuerySet iterable object.

        """
        return cls.objects.all().order_by('-created')

    @classmethod
    def get_by(cls, creator_id, target_id):
        """
        Returns a list of activities filtered by creator and target.

        Attributes:
            creator_id (int or str or None): An ID of creator.
            target_id (int or str or None): An ID of target user.

        Returns:
            A QuerySet iterable object.

        """
        activities = cls.get_all()
        if creator_id:
            activities = activities.filter(creator__id__exact=creator_id)
        if target_id:
            activities = activities.filter(target__id__exact=target_id)

        return activities

    def save(self, *args, **kwargs):
        """
        Saves correct instance of model.

        Returns:
            A boolean value indicating that this method can create
            correct activity instance.

        """
        if not self.content:  # incorrect activity, don't save
            return False
        else:  # correct activity
            super(Activity, self).save(*args, **kwargs)
            cache.delete('all_activities')  # new activity - clear cache
            return True
