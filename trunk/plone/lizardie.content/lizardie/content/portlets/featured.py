"""Define a portlet used to show featured items. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
See page 278
"""

import random

from zope.interface import Interface
from zope.interface import implements

from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

from lizardie.content.doll import IDoll

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from lizardie.content import _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class IFeatured(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)

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
                      "featured items will be preferred."),
        default=False,
        )
                            
    sitewide = schema.Bool(
        title=_(u"Sitewide featured items"),
        description=_(u"If enabled, featured items from across the "
                      "site will be found. If disabled, only "
                      "featured items in this folder and its "
                      "subfolders are eligible."),
        default=False,
        )




class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFeatured)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    def __init__(self, count=5, randomize=False, sitewide=False):
        self.count = count
        self.randomize = randomize
        self.sitewide = sitewide

    title = _(u"Featured items")

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Featured items")

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).
class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('featured.pt')

    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    @property
    def available(self):
        print "featured data length:", len(self._data())
        return len(self._data()) > 0

    # To make the view template as simple as possible, we return dicts with
    # only the necessary information.

    def featureditems(self): # was: promotions
        for brain in self._data():
            fi = brain.getObject()
            
#            scales = getMultiAdapter((fi, self.request), name='images')
#            scale = scales.scale('image', scale='thumb')
#            imageTag = None
#            if scale is not None:
#                imageTag = scale.tag()
            
            yield dict(title=fi.Title(),
                       summary=fi.Description(),
                       url=brain.getURL(),
                       )
#                       imageTag=imageTag)

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
        
        fitems = []
        if self.data.randomize:
            fitems = list(results)
            fitems.sort(lambda x,y: cmp(random.randint(0,200),100))
            fitems = fitems[:limit]
        else:
            fitems = results[:limit]
        
        return fitems



# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    form_fields = form.Fields(IFeatured)
    label = _(u"Add featured items portlet")
    description = _(u"This portlet displays featured items.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IFeatured)
    label = _(u"Edit featured items portlet")
    description = _(u"This portlet displays featured items.")


# class AddForm(base.AddForm):
#     """Portlet add form.

#     This is registered in configure.zcml. The form_fields variable tells
#     zope.formlib which fields to display. The create() method actually
#     constructs the assignment that is being added.
#     """
#     form_fields = form.Fields(IFeatured)

#     def create(self, data):
#         return Assignment(**data)


# # NOTE: IF this portlet does not have any configurable parameters, you can
# # remove this class definition and delete the editview attribute from the
# # <plone:portlet /> registration in configure.zcml

# class EditForm(base.EditForm):
#     """Portlet edit form.

#     This is registered with configure.zcml. The form_fields variable tells
#     zope.formlib which fields to display.
#     """
#     form_fields = form.Fields(IFeatured)
