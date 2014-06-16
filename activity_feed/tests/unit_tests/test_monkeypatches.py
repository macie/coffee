#-*- coding: utf-8 -*-
"""
Unit tests for monkeypatches.

"""
from __future__ import unicode_literals
import mock

from django.db.models import query
from django.test import TestCase

from activity_feed import monkeypatches


class MonkeypatchesTestCase(TestCase):
    def test_inheritanceQuerySet_get(self):
        """
        Tests inheritanceQuerySet_get function.

        """
        queryset = mock.MagicMock(spec=query.QuerySet)
        queryset.clone = queryset
        queryset.clone._result_cache = [True]
        queryset.query = mock.Mock()
        queryset.query.can_filter = mock.Mock(return_value=False)
        queryset.model = mock.Mock()
        queryset.subclasses = ''

        # one object
        queryset.__len__.return_value = 1
        queryset.filter.return_value.select_subclasses.return_value = queryset
        result = monkeypatches.inheritanceQuerySet_get(queryset)
        self.assertTrue(result)

        # more objects
        queryset.__len__.return_value = 2
        queryset.filter.return_value.select_subclasses.return_value = queryset
        with self.assertRaises(TypeError):
            # should be django.core.exceptions.ObjectDoesNotExist, but
            # checking TypeError is easier than monkeypatching
            # monkeypatched function
            monkeypatches.inheritanceQuerySet_get(queryset)

        # not number
        queryset.__len__.return_value = ''
        queryset.filter.return_value.select_subclasses.return_value = queryset
        with self.assertRaises(TypeError):
            # should be django.core.exceptions.MultipleObjectsReturned, but
            # checking TypeError is easier than monkeypatching
            # monkeypatched function
            monkeypatches.inheritanceQuerySet_get(queryset)
