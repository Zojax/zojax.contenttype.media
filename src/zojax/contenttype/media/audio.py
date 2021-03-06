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
from zojax.content.type.item import PersistentItem

from interfaces import IAudio, IStandaloneAudio
from media import Media


class Audio(Media, PersistentItem):
    interface.implements(IAudio)


class StandaloneAudio(Audio):
    interface.implements(IStandaloneAudio)
