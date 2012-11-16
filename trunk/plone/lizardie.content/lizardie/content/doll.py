from five import grok
from zope import schema
import datetime

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.app.file.interfaces import IImage # for View::images

from lizardie.content import _

class IDoll(form.Schema):
    """A doll. Dolls are managed inside Doll Folder.
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )
#    @form.validator(field=IDoll['title'])
#    def validateTitle(value):
#        if value and value == value.upper():
#            raise schema.ValidationError(u"Please don't shout")
    

    location = schema.TextLine(
        title=_(u"Location"),
        required = True
        )

    height = schema.Int(
        title=_(u"Height"),
        description=_(u"in centimeters"),
        required=True,
        min = 1,
#        searchable=False,
#        size = 2,
        )

    materials = schema.Text(
        title = _(u"Materials"),
        description = _(u"Comma-separated list of materials"),
        )

    start = schema.Date(
        title = _(u"Birthday")
        )

    nimages = schema.Int(
        title=_(u"Number of images to show before description"),
        description=_(u"Negative number means no limit"),
        required=True,
        default = -1,
        )
    body = RichText(
        title=_(u"Description"),
        description=_(u"A story about this doll"),
        required=True
        )

    status = schema.Text(
        title = _(u"Status"),
        description = _(u"Current status of the doll. If sold, specify the name and address of the customer as well as the sale date and other details."),
        )



class View(grok.View):
    """
    Default view (@@view) for Doll
    """
    grok.context(IDoll)
    grok.require('zope2.View')

    def update(self):
        """Prepare information for the template
        """
        
        self.birthdayFormatted = self.context.start.strftime("%d %b %Y")
        self.materialsFormatted = self.context.materials.split(",").sort()


    def images(self):
        """Return catalog search results of images to show"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides="Products.ATContentTypes.interfaces.image.IATImage",
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')



@form.default_value(field=IDoll['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

