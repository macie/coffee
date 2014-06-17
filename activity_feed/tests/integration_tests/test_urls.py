# -*- coding: utf-8 -*-
"""
Integration tests.

"""
from __future__ import unicode_literals

from django.test import client, SimpleTestCase


class UrlsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = client.Client()

    def test_homepage(self):
        """
        Tests home page.

        """
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # paginated
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_filtering(self):
        """
        Tests filtering.

        """
        # by creator only
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/creator/1/')
        self.assertEqual(response.status_code, 200)

        # by creator only (paginated)
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/creator/1/page/1/')
        self.assertEqual(response.status_code, 200)

        # by target only
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/target/1/')
        self.assertEqual(response.status_code, 200)

        # by target only (paginated)
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/target/1/page/1/')
        self.assertEqual(response.status_code, 200)

        # creator and target
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/creator/1/target/1/')
        self.assertEqual(response.status_code, 200)

        # creator and target (paginated)
        with self.assertTemplateUsed('admin.html'):
            response = self.client.get('/creator/1/target/1/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_filter_page(self):
        """
        Test filter page.

        """
        with self.assertTemplateNotUsed('base.html'):
            response = self.client.get('/filter/')
        self.assertRedirects(response, '/')

    def test_new_page(self):
        """
        Test create page.

        """
        with self.assertTemplateNotUsed('base.html'):
            response = self.client.get('/new/')
        self.assertRedirects(response, '/')
