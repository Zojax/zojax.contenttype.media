##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds

from zojax.batching.batch import Batch


class CategoryPage(object):

    def update(self):
        uid = getUtility(IIntIds).getId(removeAllProxies(self.context))
        ws = self.context.__parent__.__parent__

        self.medias = Batch(
            ws.medias(categories=(uid,)),
            size=ws.pageSize, request=self.request)
