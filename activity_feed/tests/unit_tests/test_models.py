#-*- coding: utf-8 -*-
"""
Unit tests for models.

"""
from __future__ import unicode_literals
import mock
from model_mommy import mommy, recipe

from django.core import exceptions
from django.test import TestCase
from django.utils import six

from activity_feed import models


class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        models.User.objects.all().delete()  # clear db

        mommy.make('Employee', _quantity=3)       # user_id = [1, 2, 3]
        mommy.make('CoffeeCompany', _quantity=2)  # user_id = [4, 5]

    def test_get_all(self):
        """
        Tests select_subclasses method.

        """
        # all user
        users = models.User.objects.select_subclasses()
        self.assertEqual(len(users), 5)

        # employees
        employees = [
            user for user in users if isinstance(user, models.Employee)]
        self.assertEqual(len(employees), 3)

        # coffee companies
        companies = [
            user for user in users if isinstance(user, models.CoffeeCompany)]
        self.assertEqual(len(companies), 2)

    def test_get_by_id(self):
        """
        Tests get method.

        """
        get_user = lambda n: models.User.objects.get(id=n)
        employee = models.Employee
        coffee_company = models.CoffeeCompany

        # get employees
        for user_id in six.moves.xrange(1, 4):
            self.assertIsInstance(get_user(user_id), employee)

        # get coffee companies
        for user_id in six.moves.xrange(4, 6):
            self.assertIsInstance(get_user(user_id), coffee_company)

        # get non-existent users
        self.assertRaises(exceptions.ObjectDoesNotExist, get_user, 0)
        self.assertRaises(exceptions.ObjectDoesNotExist, get_user, 6)


class EmployeeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        models.User.objects.all().delete()  # clear db

    def test_str(self):
        """
        Tests __str__ method.

        """
        employee = mock.MagicMock(spec=models.Employee)
        employee.first_name = 'Marek'
        employee.last_name = 'Wójcik'

        if six.PY2:
            name = models.Employee.__unicode__(employee)
        else:  # python 3
            name = models.Employee.__str__(employee)

        self.assertEqual(name, 'Marek Wójcik')

    def test_get_all(self):
        """
        Tests all method.

        """
        mommy.make('Employee', _quantity=3)       # user_id = [1, 2, 3]
        mommy.make('CoffeeCompany', _quantity=2)  # user_id = [4, 5]
        employees = models.Employee.objects.all()
        self.assertEqual(len(employees), 3)


class CoffeeCompanyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        models.User.objects.all().delete()  # clear db

    def test_str(self):
        """
        Tests __str__ method.

        """
        company = mock.MagicMock(spec=models.CoffeeCompany)
        company.full_name = 'Producent kawy'

        if six.PY2:
            name = models.CoffeeCompany.__unicode__(company)
        else:  # python 3
            name = models.CoffeeCompany.__str__(company)

        self.assertEqual(name, 'Producent kawy')

    def test_get_all(self):
        """
        Tests all method.

        """
        mommy.make('Employee', _quantity=3)       # user_id = [1, 2, 3]
        mommy.make('CoffeeCompany', _quantity=2)  # user_id = [4, 5]
        companies = models.CoffeeCompany.objects.all()
        self.assertEqual(len(companies), 2)


class ActivityTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # clear db
        models.User.objects.all().delete()
        models.Activity.objects.all().delete()

        cls.assertStrEqual = lambda cls, x, y: cls.assertEqual(str(x), str(y))

        employee = recipe.Recipe(models.Employee,
                                 id=1,
                                 first_name='Jan',
                                 last_name='Wójt')
        company = recipe.Recipe(models.CoffeeCompany,
                                id=2,
                                full_name='Kawa')
        activity1 = recipe.Recipe(models.Activity,
                                  id=1,
                                  creator=recipe.foreign_key(employee),
                                  target=recipe.foreign_key(company),
                                  content='Jan Wójt drinked coffee from Kawa')
        activity2 = recipe.Recipe(models.Activity,
                                  id=2,
                                  creator=recipe.foreign_key(company),
                                  target=recipe.foreign_key(employee),
                                  content='Kawa delivered product to Jan Wójt')

        employee.make()
        company.make()
        activity1.make()
        activity2.make()

    def test_str(self):
        """
        Tests __str__ method.

        """
        activity = mock.MagicMock(spec=models.Activity)
        activity.content = 'Ktoś zaprosił kogoś'

        if six.PY2:
            content = models.Activity.__unicode__(activity)
        else:  # python 3
            content = models.Activity.__str__(activity)

        self.assertEqual(content, 'Ktoś zaprosił kogoś')

    def test_create(self):
        """
        Tests create method.

        """
        activity = models.Activity.objects.get(id=1)

        # category, no custom_content
        new_activity = models.Activity.objects.create(
            creator_id=1,
            target_id=2,
            category='drinked coffee from')
        self.assertStrEqual(new_activity.creator, activity.creator)
        self.assertStrEqual(new_activity.target, activity.target)
        self.assertEqual(new_activity.content, activity.content)

        # no category, custom_content
        new_activity = models.Activity.objects.create(
            creator_id=1,
            target_id=2,
            custom_content='Jan Wójt drinked coffee from Kawa')
        self.assertStrEqual(new_activity.creator, activity.creator)
        self.assertStrEqual(new_activity.target, activity.target)
        self.assertEqual(new_activity.content, activity.content)

        # category, custom_content
        new_activity = models.Activity.objects.create(
            creator_id=1,
            target_id=2,
            category='drinked coffee from',
            custom_content='Should be invisible')
        self.assertStrEqual(new_activity.creator, activity.creator)
        self.assertStrEqual(new_activity.target, activity.target)
        self.assertEqual(new_activity.content, activity.content)

        # no category, no custom_content
        activity = models.Activity.objects.create(
            creator_id=1,
            target_id=2)
        self.assertStrEqual(new_activity.creator, activity.creator)
        self.assertStrEqual(new_activity.target, activity.target)
        self.assertEqual('', activity.content)

    def test_get_all(self):
        """
        Tests all method.

        """
        activities = models.Activity.objects.all()
        self.assertEqual(len(activities), 2)

    def test_get_by(self):
        """
        Tests get_by method.

        """
        # two ints
        activities = models.Activity.objects.get_by(1, 2)
        self.assertEqual(len(activities), 1)

        # two integers
        activities = models.Activity.objects.get_by('1', '2')
        self.assertEqual(len(activities), 1)

        # no target
        activities = models.Activity.objects.get_by(1, None)
        self.assertEqual(len(activities), 1)

        # no creator
        activities = models.Activity.objects.get_by(None, 2)
        self.assertEqual(len(activities), 1)

        # no target and no creator
        activities = models.Activity.objects.get_by(None, None)
        self.assertEqual(len(activities), 2)

    def test_save(self):
        """
        Tests save method.

        """
        activity = models.Activity(id=3,
                                   creator_id=1,
                                   target_id=2)

        # no content
        activity.save()
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            models.Activity.objects.get(id=3)

        # content
        activity.content = "content of activity 3"
        activity.save()
        self.assertTrue(models.Activity.objects.get(id=3))

        # cleanup
        activity.delete()
