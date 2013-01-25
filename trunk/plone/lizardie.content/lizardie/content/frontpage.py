from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from lizardie.content.doll import IDoll

from lizardie.content import _

class IFrontPage(form.Schema):
    """The front page
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
# this is associated with frontpage_templates/view.pt
class View(grok.View):
    grok.context(IFrontPage)
# permission is Zope3 permission called 'zope2.View'. Permission 'zope.Public' means 'no permission required'
# list of other standard permissions are in parts/omelette/Products/Five/permissions.zcml
    grok.require('zope2.View')
    
    def items(self):
        """Return a catalog search result of items to show
        """
        
        context = aq_parent(self.context)
        catalog = getToolByName(context, 'portal_catalog')
# http://plone.293351.n2.nabble.com/problem-when-searching-dexterity-content-with-portal-catalog-td4393561.html
        results = catalog.searchResults({'portal_type' : 'lizardie.content.doll', 'sort_on' : 'start', 'sort_order' : 'descending'})

        return results
