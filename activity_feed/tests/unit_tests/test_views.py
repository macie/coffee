#-*- coding: utf-8 -*-
"""
Unit tests for views.

"""
from __future__ import unicode_literals
import mock

from django.test import TestCase

from activity_feed import views


class ViewsTestCase(TestCase):
    def test_activities(self):
        """
        Tests activities function.

        """
        request = mock.Mock()
        request.META = {}

        # no explicit args (no ajax)
        response = views.activities(request)
        self.assertEqual(response.status_code, 200)  # render page

        # page not a number
        response = views.activities(request, page='')
        self.assertEqual(response.status_code, 200)  # render page

        # page out of range
        response = views.activities(request, page=100000)
        self.assertEqual(response.status_code, 200)  # render page

        # ajax
        request.is_ajax = mock.Mock(return_value=True)
        response = views.activities(request)
        self.assertEqual(response.status_code, 200)  # render activity list

        # no ajax
        request.is_ajax = mock.Mock(return_value=False)
        response = views.activities(request)
        self.assertEqual(response.status_code, 200)  # render page

    def test_create_activity_GET(self):
        """
        Tests create_activity function with GET request.

        """
        request = mock.Mock()
        request.method = 'GET'

        response = views.create_activity(request)
        self.assertEqual(response.status_code, 302)  # redirect

    def test_create_activity_POST(self):
        """
        Tests create_activity function with POST request.

        """
        request = mock.Mock()
        request.method = 'POST'
        request.POST = {'creator': '1',
                        'target': '2',
                        'category': '',
                        'content': ''}

        # no ajax
        request.is_ajax = mock.Mock(return_value=False)
        response = views.create_activity(request)
        self.assertEqual(response.status_code, 302)  # redirect

        # ajax and no activity (no content)
        request.is_ajax = mock.Mock(return_value=True)
        response = views.create_activity(request)
        self.assertEqual(response.content, '\n\n\n\n\n\t\t\t\t\n\t\t\t\t<li>\n\t\t\t\t\t<div></div>\n\t\t\t\t\t<div class="time">None</div>\n\t\t\t\t</li>\n\t\t\t\t\n\n\n\n\n')  # empty string

        # ajax and no activity (create error)
        request.is_ajax = mock.Mock(return_value=True)
        with mock.patch(
                'activity_feed.views.models.Activity.objects.create') as m:
            m.return_value = False
            response = views.create_activity(request)
            self.assertEqual(response, '')  # empty response

        # ajax and activity
        request.is_ajax = mock.Mock(return_value=True)
        request.POST['content'] = 'some content'
        response = views.create_activity(request)
        self.assertEqual(response.status_code, 200)  # list render

    def test_filter_activities_GET(self):
        """
        Tests filter_activities function with GET request.

        """
        request = mock.Mock()
        request.method = 'GET'
        request.GET = {'creator': '',
                       'target': ''}

        response = views.filter_activities(request)
        self.assertEqual(response.status_code, 302)  # redirect

    def test_filter_activities_POST(self):
        """
        Tests filter_activities function with POST request.

        """
        request = mock.Mock()
        request.method = 'POST'
        request.POST = {}

        response = views.filter_activities(request)
        self.assertEqual(response.status_code, 302)  # redirect

    def test_create_filter_uri(self):
        """
        Tests _create_filter_uri function.

        """
        creator_id = 1
        target_id = 2

        # both (integers)
        uri = '/creator/{}/target/{}/'.format(creator_id, target_id)
        result = views._create_filter_uri(creator_id, target_id)
        self.assertEqual(result, uri)

        # both (strings)
        uri = '/creator/{}/target/{}/'.format(creator_id, target_id)
        result = views._create_filter_uri(str(creator_id), str(target_id))
        self.assertEqual(result, uri)

        # creator, no target
        uri = '/creator/{}/'.format(creator_id)
        result = views._create_filter_uri(creator_id, None)
        self.assertEqual(result, uri)

        # no creator, target
        uri = '/target/{}/'.format(target_id)
        result = views._create_filter_uri(None, target_id)
        self.assertEqual(result, uri)

        # no creator, no target
        uri = '/'
        result = views._create_filter_uri(None, None)
        self.assertEqual(result, uri)
