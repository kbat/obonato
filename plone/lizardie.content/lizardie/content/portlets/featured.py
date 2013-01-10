"""Define a portlet used to show featured items. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
See page 278.
"""

import random

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from lizardie.content.featured import IFeatured
from lizardie.content import MessageFactory as _

# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class IFeaturedItemsPortlet(IPortletDataProvider):

    count = schema.Int(
            title=_(u"Number of featured items to display"),
            description=_(u"Maximum number of featured items to show"),
            required=True,
            default=5,
        )
                       
    randomize = schema.Bool(
            title=_(u"Randomize featured items"),
            description=_(u"If enabled, featured items to show will"
                            "be picked randomly. If disabled, newer "
                            "items will be preferred."),
            default=False,
        )
                            
    sitewide = schema.Bool(
            title=_(u"Sitewide items"),
            description=_(u"If enabled, featured items from across the "
                           "site will be found. If disabled, only "
                           "items in this folder and its "
                           "subfolders are eligible."),
            default=False,
        )

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(IFeaturedItemsPortlet)

    def __init__(self, count=5, randomize=False, sitewide=False):
        self.count = count
        self.randomize = randomize
        self.sitewide = sitewide

    title = _(u"Featured items") # defined in portlets.interfaces.IPortletAssignment, declared by base.Assignment. It is possible to use a dynamic @property for this, if required

# The renderer is like a view (in fact, like a content provider/viewlet) exchept that it only renders a part of a page
# The item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).
# This class describes most of the logic of the portlet.

class Renderer(base.Renderer):

    # render() will be called to render the portlet - see page 282
    
    render = ViewPageTemplateFile('featured.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    @property
    def available(self): # see page 282 "Portlet renderers"
        return len(self._data()) > 0

    # To make the view template as simple as possible, we return dicts with
    # only the necessary information.

    def featured(self):
        for brain in self._data():
            fi = brain.getObject()
            
            scales = getMultiAdapter((fi, self.request), name='images')
            scale = scales.scale('image', scale='thumb')
            imageTag = None
            if scale is not None:
                imageTag = scale.tag()
            
            yield dict(title=fi.Title(),
                       summary=fi.Description(),
                       url=brain.getURL(),
                       imageTag=imageTag)

    # By using the @memoize decorator, the return value of the function will
    # be cached. Thus, calling it again does not result in another query.
    # See the plone.memoize package for more.
        
    @memoize
    def _data(self):
        limit = self.data.count
        
        query = dict(object_provides=IDoll.__identifier__)
        
        if not self.data.sitewide:
            query['path'] = '/'.join(self.context.getPhysicalPath())
        if not self.data.randomize:
            query['sort_on'] = 'modified'
            query['sort_order'] = 'reverse'
            query['sort_limit'] = limit
        
        # Ensure that we only get active objects, even if the user would
        # normally have the rights to view inactive objects (as an
        # administrator would)
        query['effectiveRange'] = DateTime()
        
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        
        featured = []
        if self.data.randomize:
            featured = list(results)
            featured.sort(lambda x,y: cmp(random.randint(0,200),100))
            featured = featured[:limit]
        else:
            featured = results[:limit]
        
        return featured

# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.AddForm):
    form_fields = form.Fields(IFeaturedItemsPortlet)
    label = _(u"Add Featured portlet")
    description = _(u"This portlet displays featured items.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IFeaturedItemsPortlet)
    label = _(u"Edit Featured portlet")
    description = _(u"This portlet displays featured items.")
