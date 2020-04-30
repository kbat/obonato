# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from cl.content.content.component import IComponent
from zope.interface import implementer
from Acquisition import aq_inner

class ILibrary(model.Schema):
    """ Marker interface for Library
    """

@implementer(ILibrary)
class Library(Container):
    """
    """

class View(BrowserView):
    """ Browser view class
    """

    def components(self):
        """ Return catalogue search result of components """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=IComponent.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title',
                       sort_order='descending')
