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
from zope import interface, component
from zope.component import getUtility
from zope.event import notify
from zope import size
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.content.type.container import ContentContainer
from zojax.content.space.interfaces import IContentSpace
from zojax.catalog.interfaces import ICatalog

from interfaces import _, IMediaWorkspace, IMediaWorkspaceFactory
from category import CategoryContainer

class MediaWorkspace(ContentContainer):
    interface.implements(IMediaWorkspace)

    title = u'Media'
    pageSize = 10
    subspaces = False

    @property
    def space(self):
        return self.__parent__

    def medias(self, categories=None):
        catalog = getUtility(ICatalog)

        query = dict(
            draftContent = {'any_of': (False,)},
            sort_on='modified', sort_order='reverse',
            contentTypeIsMedia = {'any_of': (True, )}
        )

        if categories:
            query['contentTypeMediaCategoryIds'] = {'any_of': set(categories)}

        if self.subspaces:
            query['traversablePath'] = {'any_of': (self.space,)}
        else:
            query['contentSpace'] = {'any_of': (self.space.id,)}
        return catalog.searchResults(**query)

@component.adapter(IMediaWorkspace, IObjectAddedEvent)
def mediaWorkspaceAdded(ws, event):
    if 'category' not in ws:
        category = CategoryContainer()
        notify(ObjectCreatedEvent(category))
        ws['category'] = category

class MediaSized(object):
    component.adapts(IMediaWorkspace)
    interface.implements(size.interfaces.ISized)

    def __init__(self, context):
        self.context = context
        self._size = len(self.context.medias())

    def sizeForSorting(self):
        return "media(s)", self._size

    def sizeForDisplay(self):
        return size.byteDisplay(self._size)

class MediaWorkspaceFactory(object):
    component.adapts(IContentSpace)
    interface.implements(IMediaWorkspaceFactory)

    name = 'media'
    title = u'Media'
    description = u'A media workspace that will show all space medias.'
    weight = 2

    def __init__(self, space):
        self.space = space

    def get(self):
        return self.space.get('media')

    def install(self):
        ws = self.space.get('media')

        if not IMediaWorkspace.providedBy(ws):
            ws = MediaWorkspace(title = u"Media")
            notify(ObjectCreatedEvent(ws))
            removeSecurityProxy(self.space)['media'] = ws
            notify(ObjectModifiedEvent(self.space))

        return self.space['media']

    def uninstall(self):
        del self.space['media']

    def isInstalled(self):
        return 'media' in self.space

    def isAvailable(self):
        return True
