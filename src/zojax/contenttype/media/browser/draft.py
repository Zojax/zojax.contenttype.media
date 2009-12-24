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
from zope import interface
from zope.proxy import removeAllProxies
from zope.component import getUtility, getMultiAdapter
from zojax.wizard import WizardStepForm
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.content.type.interfaces import IItem, IContentType
from zojax.layoutform import button, Fields, PageletForm, PageletEditSubForm
from zojax.blogger.interfaces import _


class MediaCategoryStep(WizardStepForm):

    title = _(u'Category')


class AddMediaCategory(PageletForm):

    label = u'Add category'
    prefix = 'newsitem.add.category'
    fields = Fields(IItem).omit('description')
    ignoreContext = True

    def update(self):
        category = self.context['category']
        ct = getUtility(IContentType, 'contenttype.media.category').__bind__(category)

        self.ct = ct
        super(AddMediaCategory, self).update()

    @button.buttonAndHandler(_('Add'))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            IStatusMessage(self.request).add('Please fix indicated error.')
        else:
            category = self.ct.create(**data)
            self.ct.add(category)
            IStatusMessage(self.request).add('Category has been added.')
            self.widgets['title'].value = u'' # clear after adding
