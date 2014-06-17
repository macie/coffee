# -*- coding: utf-8 -*-
"""
Monkeypatches for third-party django libraries.

"""
from model_utils import managers


def inheritanceQuerySet_get(self, *args, **kwargs):
    """
    Extends model_utils.managers.InheritanceQuerySet to ForeignKey support.

    More info: https://github.com/carljm/django-model-utils/issues/11

    """
    clone = self.filter(*args, **kwargs).select_subclasses()
    if not hasattr(self, 'subclasses'):
        clone = clone.select_subclasses()

    if self.query.can_filter():
        clone = clone.order_by()
    num = len(clone)
    if num == 1:
        return clone._result_cache[0]
    if not num:
        raise self.model.DoesNotExist(
            "%s matching query does not exist." %
            self.model._meta.object_name)
    raise self.model.MultipleObjectsReturned(
        "get() returned more than one %s -- it returned %s!" %
        (self.model._meta.object_name, num))

managers.InheritanceQuerySet.get = inheritanceQuerySet_get
InheritanceManager = managers.InheritanceManager
