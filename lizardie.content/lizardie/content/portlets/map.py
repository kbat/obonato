"""Define a portlet used to show map of dolls. This follows the patterns from
plone.app.portlets.portlets. Note that we also need a portlet.xml in the
GenericSetup extension profile to tell Plone about our new portlet.
See page 278
"""

from zope.interface import Interface
from zope.interface import implements

from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
#from plone.namedfile.interfaces import IImageScaleTraversable
#from plone.namedfile.field import NamedBlobImage

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from lizardie.content import _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class IMap(IPortletDataProvider):
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

    # image = NamedBlobImage(
    #     title=_(u"Map of dolls"),
    #     description=_(u"An image with the map of dolls"),
    #     required=True,
    #     )




class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMap)

    def __init__(self):
        pass

    title = _(u"Map of dolls")

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Map of dolls")

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

    render = ViewPageTemplateFile('map.pt')

    # The 'available' property is used to determine if the portlet should
    # be shown.
        
    @property
    def available(self):
        return True


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    form_fields = form.Fields(IMap)
    label = _(u"Add map portlet")
    description = _(u"This portlet displays map of dolls.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IMap)
    label = _(u"Edit the Map portlet")
    description = _(u"This portlet displays map of dolls.")
