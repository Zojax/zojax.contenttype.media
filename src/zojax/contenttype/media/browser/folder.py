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
from zope.app.component.hooks import getSite
from zope.interface import Interface
from zope.component import getUtility, getUtilitiesFor
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IZopeDublinCore

from zojax.table.table import Table
from zojax.catalog.interfaces import ICatalog
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.utils import getSpace
from zojax.content.table.interfaces import IContentsTable
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.ownership.interfaces import IOwnership
from zojax.content.actions.contentactions import BrowseContentAction
from zojax.contenttype.media.interfaces import _, IMediaWorkspace, IMediaType

from interfaces import IBrowseMediaAction


class MediaTable(Table):
    interface.implements(IContentsTable)
    component.adapts(Interface, Interface, Interface)

    title = _('Media')

    pageSize = 15
    enabledColumns = ('author', 'title', 'type', 'location', 'modified')
    msgEmptyTable = _('No content has been added yet.')

    def initDataset(self):
        types = [name for name, ct in getUtilitiesFor(IMediaType)]

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': types},
            sort_order='reverse', sort_on='modified',
            isDraft={'any_of': (False,)})

        self.dataset = results


class SpaceMediaTable(MediaTable):
    component.adapts(IContentSpace, Interface, Interface)

    enabledColumns = ('author', 'title', 'type', 'space', 'modified')


class BrowseMediaAction(BrowseContentAction):
    interface.implements(IBrowseMediaAction)

    title = _('Browse media')
    weight = 100
    contextInterface = IContentSpace

    @property
    def url(self):
        return '%s/browse-media.html'%absoluteURL(self.context, self.request)


class MediaContainerItem(object):

    def update(self):
        self.date = IZopeDublinCore(self.context).created
        self.site_url = absoluteURL(getSite(), self.request)
        self.space = getSpace(self.context)
        owner = IOwnership(self.context).owner
        space = IPersonalSpace(owner, None)
        profile = IPersonalProfile(owner, None)
        self.container_url = absoluteURL(self.space, self.request)
        # author
        try:
            self.author = '%s %s'%(profile.firstname, profile.lastname)
            self.avatar_url = profile.avatarUrl(self.request)
        except AttributeError:
            self.author = getattr(owner,'title','')
            self.avatar_url = '#'

        if space is not None:
            self.profile_url = '%s/profile/'%absoluteURL(space, self.request)
        self.container_title = self.space.title
