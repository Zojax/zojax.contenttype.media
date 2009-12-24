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
from operator import attrgetter
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from zojax.cache.view import cache
from zojax.cache.keys import Context
from zojax.batching.batch import Batch

from zojax.contenttype.media.cache import MediaItemsTag


def MediaListingBatchTag(oid, instance, *args, **kw):
    return {'bstart': (instance.medias.start, len(instance.medias)),
            'bpages': len(instance.medias.batches),
            'context': getPath(instance.context)}


class MediaListing(object):

    def update(self):
        self.medias = Batch(
            self.context.medias(),
            size=self.context.pageSize, request=self.request)

        self.intids = getUtility(IIntIds)

    def getCategories(self, item):
        queryObject = self.intids.queryObject
        categories = []
        for uid in item.category:
            category = queryObject(uid)
            if category is not None:
                categories.append(category)
        categories.sort(key=attrgetter('title'))
        return categories

    @cache('zojax.contenttype.media.mediamodel.view', MediaItemsTag, MediaListingBatchTag)
    def updateAndRender(self):
        return super(MediaListing, self).updateAndRender()
