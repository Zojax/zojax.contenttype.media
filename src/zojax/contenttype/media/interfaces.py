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
""" video content type interfaces

$Id$
"""
from zope import schema, interface
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from z3c.schema.baseurl import BaseURL
from zojax.richtext.field import RichText
from zojax.filefield.field import FileField, ImageField
from zojax.widget.list.field import SimpleList
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.type.interfaces import IItem
from zojax.contenttypes.interfaces import _
from zojax.widget.checkbox.field import CheckboxList
from zojax.jquery.media.mediatypes.field import MediaTypeChoice

positionVoc = SimpleVocabulary((
    SimpleTerm(1, '1', _('Above media')),
    SimpleTerm(2, '2', _('Under media'))))


class ICategory(IItem):
    """ news item category """


class ICategoryContainer(interface.Interface):
    """ media item category container """


class IMedia(IItem):
    """ Media type """

    mediaSource = schema.Text(
        title = _(u'Media source'),
        description = _(u'HTML to link to Media.'),
        required = False)

    mediaURL = schema.URI(
        title = _(u'Media URL'),
        description = _(u'Link to Media.'),
        required = False)

    mediaURLList = SimpleList(
        title = _(u'Media URL List'),
        description = _(u'List of Links to Media, will be used as playlist. Makes sense only for mp3 or flv types'),
        required = False)

    mediaData = FileField(
        title=_(u'Media data'),
        description=_(u'Upload the media content.'),
        required = False)

    mediaType = MediaTypeChoice(
        title = _(u'Media type'),
        description = _(u'Media type, i.e. flv, etc.'),
        required = True)

    text = RichText(
        title = _(u'Body'),
        description = _(u'Media body text.'),
        required = False)

    position = schema.Choice(
        title = _(u'Text position'),
        description = _(u'Put text above or under media.'),
        vocabulary = positionVoc,
        default = 1,
        required = False)

    width = schema.Int(
        title = _(u'Width'),
        description = _(u'Media content width.'),
        required = False,
        default=400)

    height = schema.Int(
        title = _(u'Height'),
        description = _(u'Media content height.'),
        required = False,
        default=300)

    autoplay = schema.Bool(
        title = _(u'Autoplay'),
        description = _(u'Autoplay.'),
        required = True,
        default=False)

    category = CheckboxList(
        title = _(u'Category'),
        description = _('Select category for the media.'),
        vocabulary = 'zojax.contenttype.media-categories',
        default = [],
        required = False)


class IAudio(IMedia):
    """ Audio type """


class IStandaloneAudio(IAudio):
    """ Standalone audio type """


class IVideo(IMedia):
    """ Video type """

    preview = ImageField(
        title = _(u'Preview'),
        description = _(u'Preview image.'),
        required = False)


class IStandaloneVideo(IVideo):
    """ Standalone video type """


class IMediaContainer(IItem):
    """ Media container """


class IMediaContainerType(interface.Interface):
    """ Media container type """

class IMediaType(interface.Interface):
    """ media content type """

class IStandaloneMediaType(interface.Interface):
    """ standalone media content type """


class IVideoType(interface.Interface):
    """ video content type """


class IStandaloneVideoType(interface.Interface):
    """ standalone video content type """


class IAudioType(interface.Interface):
    """ audio content type """


class IStandaloneAudioType(interface.Interface):
    """ standalone audio content type """


class IMediaWorkspace(IWorkspace):
    """ media workspace """

    pageSize = schema.Int(
        title = _(u'Page size'),
        description = _(u'Number of medias items per page.'),
        default = 15,
        required = True)

    subspaces = schema.Bool(
        title = _(u'Sub spaces'),
        description = _(u'Show media for all sub-spaces or just for current space.'),
        default = False,
        required = True)

    def medias(categories=None):
        """ list media items

        categories argument is a set of category IDs that can be passed
        to filter media items.
        """


class IMediaWorkspaceFactory(IWorkspaceFactory):
    """ media workspace factory """


class IMediaItemView(interface.Interface):
    """ media item view """
