from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from irwilot.content.exhibition import IExhibition

from irwilot.content import _

class IExhibitionFolder(form.Schema):
    """A exhibition folder.
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        )
    
    details = RichText(
        title=_(u"Text"),
        required=False
        )


# View registration:
# http://plone.org/products/dexterity/documentation/manual/developer-manual/custom-views/referencemanual-all-pages
# the view name is @view taken from the class name in lowercase
# this is associated with exhibitionfolder_templates/view.pt
class View(grok.View):
    grok.context(IExhibitionFolder)
# permission is Zope3 permission called 'zope2.View'. Permission 'zope.Public' means 'no permission required'
# list of other standard permissions are in parts/omelette/Products/Five/permissions.zcml
    grok.require('zope2.View')
    
    def exhibitions(self):
        """Return a catalog search result of exhibitions to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=IExhibition.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='start',
                       sort_order='descending')
