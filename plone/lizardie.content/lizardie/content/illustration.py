from five import grok
from zope import schema
import datetime

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
# from zope.app.file.interfaces import IImage # for View::images
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer

from lizardie.content import _

from zope.interface import implements
from zope.interface import Interface
from plone.memoize.instance import memoize

class IIllustration(form.Schema):
    """An illustration. Illustrations are managed inside Illustration Folder.
    """

    # Main form
    
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )
    
    start = schema.Date(
        title = _(u"Birthday"),
        required = True,
        )

    image = NamedBlobImage(
        title = _(u"Picture"),
        required = True,
        )

    dexteritytextindexer.searchable('body')
    body = RichText(
        title=_(u"Description"),
        description=_(u"A story about this illustration"),
        required=False,
        )

    dexteritytextindexer.searchable('notes')
    notes = schema.Text(
        title = _(u"Notes"),
        description = _(u"Visible to registered users only"),
        required = False,
        )

    # Properties fieldset
    form.fieldset('nondigital', label=_(u"Non-digital"), description=_(u"Properties of non-digital images"), fields=['width', 'height', 'materials'])

    width = schema.Int(
        title=_(u"Width"),
        description=_(u"in centimeters"),
        required=False,
        min = 1,
        )

    height = schema.Int(
        title=_(u"Height"),
        description=_(u"in centimeters"),
        required=False,
        min = 1,
        )

    dexteritytextindexer.searchable('materials')
    materials = schema.Text(
        title = _(u"Materials"),
        description = _(u"Comma-separated list of materials"),
        required = False,
        )


    # Links fieldset

    form.fieldset('links', label=_(u"Links"), fields=['links'])

    form.widget(links=TextLinesFieldWidget)
    links = schema.List(
        title = _(u"Links"),
        description = _(u'Various links with this illustration, one per line'),
        value_type = schema.TextLine(),
        required = False,
        )



# We inherit the View class from dexterity.DisplayForm instead of grok.View in order to be able to show the related items
# as suggested here: http://stackoverflow.com/questions/6920817/rendering-related-items-of-a-dexterity-content-type
class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for a illustration.
    The associated template is found in illustration_templates/view.pt.
    """

    implements(IIllustration)
    grok.context(IIllustration)
    grok.require('zope2.View')

    def update(self):
        """Prepare information for the template
        """
        self.birthdayFormatted = self.context.start.strftime("%d %b %Y")
        self.materialsFormatted = None
        if self.context.materials: self.materialsFormatted = self.context.materials.split(",").sort()
#        self.context.image = self.context.picture # to be able to treat illustration as image in TinyMCE
        self.context.picture = self.context.image # temporary before I fixed templates
        
    def mainimage(self):
        """Return image to show in IllustrationFolder view
           Use the following code to call this method from the parent folder: <img tal:define="obj illustration/getObject; image python: obj.restrictedTraverse('@@view').mainimage()"
           [page 182]
        """

        return self.context.picture

@form.default_value(field=IIllustration['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

# Works but only the standard message is shown
#@form.validator(field=IIllustration['title'])
#def validateTitle(value):
#    if value and value == value.upper():
#        raise schema.ValidationError(_(u"Please don't shout"))
