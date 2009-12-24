##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
""" video implementation

$Id$
"""
from zope import interface, component
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.schema.fieldproperty import FieldProperty
from zojax.content.type.item import PersistentItem
from zojax.content.type.searchable import ContentSearchableText
from zojax.richtext.field import RichTextProperty
from zojax.filefield.field import FileFieldProperty

from interfaces import IMedia


class Media(object):
    interface.implements(IMedia)

    text = RichTextProperty(IMedia['text'])

    category = FieldProperty(IMedia['category'])

    width = FieldProperty(IMedia['width'])

    height = FieldProperty(IMedia['height'])

    autoplay = FieldProperty(IMedia['autoplay'])

    mediaData = FileFieldProperty(IMedia['mediaData'])

    mediaSource = FieldProperty(IMedia['mediaSource'])

    mediaURLList = FieldProperty(IMedia['mediaURLList'])

    position = FieldProperty(IMedia['position'])


class Sized(object):
    component.adapts(IMedia)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

        self.size = len(context.title) + \
                    len(context.description) + \
                    (context.text is not None and len(context.text) or 0) + \
                    (context.mediaData is not None and len(context.mediaData) or 0)

    def sizeForSorting(self):
        return "byte", self.size

    def sizeForDisplay(self):
        return byteDisplay(self.size)


class MediaSearchableText(ContentSearchableText):
    component.adapts(IMedia)

    def getSearchableText(self):
        text = super(MediaSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text
