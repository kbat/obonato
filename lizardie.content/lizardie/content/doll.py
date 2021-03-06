from five import grok
from zope import schema
import datetime

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
# from zope.app.file.interfaces import IImage # for View::images
from plone.z3cform.textlines.textlines import TextLinesFieldWidget

# next 2 lines are for indexing
from collective import dexteritytextindexer
from zope.interface import alsoProvides

from lizardie.content import _

from zope.interface import implements
from zope.interface import Interface
from plone.memoize.instance import memoize

class IDoll(form.Schema):
    """A doll. Dolls are managed inside Doll Folder.
    """

    # Main form
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )
#    @form.validator(field=IDoll['title'])
#    def validateTitle(value):
#        if value and value == value.upper():
#            raise schema.ValidationError(u"Please don't shout")
    

    dexteritytextindexer.searchable('location')
    location = schema.TextLine(
        title=_(u"Location"),
        required = True,
        )

    height = schema.Int(
        title=_(u"Height"),
        description=_(u"in centimeters"),
        required=True,
        min = 1,
#        searchable=False,
#        size = 2,
        )

    dexteritytextindexer.searchable('materials')
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

    form.primary('body') # what does it mean? has it anything to do with mounting or external editing?
    dexteritytextindexer.searchable('body')
    body = RichText(
        title=_(u"Description"),
        description=_(u"A story about this doll"),
        required=True,
        )

    dexteritytextindexer.searchable('status')
    status = schema.Text(
        title = _(u"Status"),
        description = _(u"Current status of the doll. If sold, specify the name and address of the customer as well as the sale date and other details."),
        )

    # Links fieldset

    form.fieldset('links', label=_(u"Links"), fields=['links'])

    form.widget(links=TextLinesFieldWidget)
    dexteritytextindexer.searchable('links')
    links = schema.List(
        title = _(u"Links"),
        description = _(u'Various links with this doll, one per line'),
        value_type = schema.TextLine(),
        required = False,
        )



# We inherit the View class from dexterity.DisplayForm instead of grok.View in order to be able to show the related items
# as suggested here: http://stackoverflow.com/questions/6920817/rendering-related-items-of-a-dexterity-content-type
class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for a doll.
    The associated template is found in doll_templates/view.pt.
    """

    implements(IDoll)
    grok.context(IDoll)
    grok.require('zope2.View')

    def update(self):
        """Prepare information for the template
        """
        
        self.birthdayFormatted = self.context.start.strftime("%d %b %Y")
        self.materialsFormatted = self.context.materials.split(",").sort()
#        self.context.image = self.mainimage() # to be able to treat doll as image in TinyMCE


    @memoize # [page 259]
    def images(self):
        """Return catalog search results of images to show
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides="Products.ATContentTypes.interfaces.image.IATImage",
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='getObjPositionInParent',
                       )
#                       sort_limit=limit)[:limit] # sort_limit is only a hint for the search algorithms and can potentially return more items, so we also use slicing
#                       sort_on='sortable_title')

    def imagesLimited(self):
        """Return catalog search results of images to show limited by context.nimages
        """
        images = self.images()
        if self.context.nimages < 0:
            return images
        else:
            return images[:self.context.nimages]

    def mainimage(self):
        """Return image to show in DollFolder view
           Use the following code to call this method from the parent folder: <img tal:define="obj doll/getObject; image python: obj.restrictedTraverse('@@view').mainimage()"
           [page 182]
        """

        return self.images()[0]


@form.default_value(field=IDoll['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

