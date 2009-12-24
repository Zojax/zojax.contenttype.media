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
"""News item view

$Id$
"""
import urllib
from operator import attrgetter
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.dublincore.interfaces import IZopeDublinCore
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from zojax.layout.pagelet import BrowserPagelet
from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.content.discussion.interfaces import IContentDiscussion
from zojax.content.tagging.interfaces import IContentTags
from zojax.content.space.utils import getSpace
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.ownership.interfaces import IOwnership
from zojax.resourcepackage.library import include


class MediaPage(object):

    media = ViewPageTemplateFile('media.pt')
    profile_url = ''

    mediaURLList = []
    mediaURLListEncoded = ''

    def update(self):
        queryObject = getUtility(IIntIds).queryObject
        self.categories = categories = []
        for uid in self.context.category:
            category = queryObject(uid)
            if category is not None:
                categories.append(category)
        categories.sort(key=attrgetter('title'))
        self.date = IZopeDublinCore(self.context).created
        self.autoplay = str(self.context.autoplay).lower()

        if self.context.mediaSource:
            self.mediaURL = None
        else:
            self.mediaURL = (self.context.mediaData is not None \
                             and self.context.mediaData.data) \
                            and '%s/view.html' % absoluteURL(self.context, self.request) \
                            or (self.context.mediaURL or '')
            self.mediaURLEncoded = urllib.quote(self.mediaURL)
            if self.context.mediaURLList:
                self.mediaURL = self.context.mediaURLList[0]
                urls = map(lambda x: r"""{\'url\':\'%s\', \'autoPlay\': %s}""" % (urllib.quote(x[1]), \
                                                                                     x[0]==0 and self.autoplay or 'true'), \
                                                enumerate(self.context.mediaURLList))
                self.mediaURLListEncoded = r"\'playlist\': [ %s]" % ','.join(urls)
            else:
                self.mediaURLListEncoded = r"\'playlist\': [ %s]" % self.mediaURLEncoded
        #\'clip\': {\'url\':\'${view/mediaURLEncoded}\', \'autoPlay\': ${view/autoplay}, \'autoBuffering\': true }
        discussion = IContentDiscussion(self.context, None)
        self.comments = discussion is not None and len(discussion)
        self.discussible = discussion is not None and discussion.status != 3
        self.addcomment = self.discussible and discussion.status != 2
        self.tags = IContentTags(self.context, None)
        self.tags = self.tags is not None and self.tags.tags or []
        self.url = absoluteURL(self.context, self.request)
        self.space = getSpace(self.context)
        self.container_url = absoluteURL(self.space, self.request)
        self.site_url = absoluteURL(getSite(), self.request)
        owner = IOwnership(self.context).owner
        space = IPersonalSpace(owner, None)
        profile = IPersonalProfile(owner, None)
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
        include('jquery-plugins')

    @cache('zojax.contenttype.media.item.view', ContextModified)
    def updateAndRender(self):
        return super(MediaPage, self).updateAndRender()


class MediaDownload(object):

    def show(self):
        if self.context.mediaData is not None:
            return self.context.mediaData.show(
                self.request,
                filename=self.context.__name__,
                contentDisposition='inline')
