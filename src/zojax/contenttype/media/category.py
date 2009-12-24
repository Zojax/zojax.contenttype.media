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
from zope.component import adapter, getUtility, getAdapter, queryAdapter
from zope.event import notify
from zope.interface import implements, implementer
from zope.lifecycleevent import ObjectCreatedEvent
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.intid.interfaces import IIntIds

from zojax.catalog.interfaces import ICatalog
from zojax.content.draft.interfaces import IDraftContent
from zojax.content.space.interfaces import ISpace, IWorkspaceFactory
from zojax.content.type.interfaces import ISearchableContent
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.portal.interfaces import IPortal

from interfaces import (
    ICategory,
    ICategoryContainer,
    IMediaWorkspace,
    IMedia)


class Category(PersistentItem):
    implements(ICategory, ISearchableContent)


class CategoryContainer(ContentContainer):
    implements(ICategoryContainer)

    title = u'Categories'


@implementer(IVocabularyFactory)
def CategoryIdsVocabulary(context):

    while True:

        if ISpace.providedBy(context):
            break

        if IDraftContent.providedBy(context):
            context = context.getLocation()
            break

        context = getattr(context, '__parent__', None)
        if context is None:
            break

    if context is None:
        return SimpleVocabulary(())

    getId = getUtility(IIntIds).getId
    terms = []

    while True:

        ws = queryAdapter(context, IWorkspaceFactory, name='media')

        if ws is not None and ws.isInstalled():
            for category in context['media']['category'].values():
                id = getId(removeAllProxies(category))
                term = SimpleTerm(id, str(id), category.title)
                term.description = category.description
                terms.append(term)

        if IPortal.providedBy(context):
            break

        context = getattr(context, '__parent__', None)
        if context is None or not ISpace.providedBy(context):
            break

    terms.sort(key=lambda t:t.title)

    return SimpleVocabulary(terms)

@implementer(IVocabularyFactory)
def PortalCategoryIdsVocabulary(context=None):
    result = getUtility(ICatalog).searchResults(type={'any_of': ('contenttype.media.category', )})
    getObject = result.uidutil.getObject

    terms = []

    for uid in result.uids:
        category = getObject(uid)
        term = SimpleTerm(uid, str(uid), category.title)
        term.description = category.description
        terms.append(term)

    terms.sort(key=lambda t:t.title)

    return SimpleVocabulary(terms)
