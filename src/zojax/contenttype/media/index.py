##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from pytz import utc
from datetime import datetime
from zc.catalog.catalogindex import ValueIndex, SetIndex
from zojax.catalog.utils import Indexable
from interfaces import IMediaType, IMedia


def indexIsMedia():
    return ValueIndex(
        'value', Indexable('zojax.contenttype.media.index.IsMedia'))

def indexMediaCategoryIds():
    return SetIndex(
        'value', Indexable('zojax.contenttype.media.index.MediaCategoryIds'))


class IsMedia(object):

    def __init__(self, context, default=None):
        self.value = IMediaType.providedBy(context)


class MediaCategoryIds(object):

    def __init__(self, context, default=None):
        item = IMedia(context, None)
        if item is None or getattr(item, 'category', None) is None:
            self.value = default
        else:
            self.value = set(item.category)
