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

from irwilot.content import _

from zope.interface import implements
from zope.interface import Interface
from plone.memoize.instance import memoize

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

genre_voc = SimpleVocabulary(
    [   SimpleTerm(value=u'landscape', title=_(u'Landscape')),
        SimpleTerm(value=u'portrait', title=_(u'Portrait')),
        SimpleTerm(value=u'stilllife', title=_(u'Still life')),
        SimpleTerm(value=u'fantasy', title=_(u'Fantasy')),
        SimpleTerm(value=u'composition', title=_(u'Composition')) ]
    )

style_voc = SimpleVocabulary(
    [   SimpleTerm(value=u'realism', title=_(u'Realism')),
        SimpleTerm(value=u'impressionism', title=_(u'Impressionism'))  ]
    )

technique_voc = SimpleVocabulary(
    [   SimpleTerm(value=u'oil', title=_(u'Oil')),
        SimpleTerm(value=u'watercolour', title=_(u'Water-colour'))  ]
    )


class IIllustration(form.Schema):
    """An illustration. Illustrations are managed inside Illustration Folder.
    """

    # Main form
    
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )
    
    # description = schema.Text(
    #     title = _(u"Description"),
    #     description = _(u"test of Description"),
    #     required = False,
    #     )

    start = schema.Date(
        title = _(u"Birthday"),
        required = True,
        )

    image = NamedBlobImage(
        title = _(u"Picture"),
        required = True,
        )

    width = schema.Int(
        title=_(u"Width"),
        description=_(u"in centimeters"),
        required=True,
        min = 1,
        )

    height = schema.Int(
        title=_(u"Height"),
        description=_(u"in centimeters"),
        required=True,
        min = 1,
        )

    genre = schema.Choice(
        title = _(u"Genre"),
        vocabulary = genre_voc,
        required = True,
        )

    style = schema.Choice(
        title = _(u"Style"),
        description = _(u"Style of the illustration"),
        vocabulary = style_voc,
        required = True,
        )

    technique = schema.Choice(
        title = _(u"Technique"),
        description = _(u"Technique of the illustration"),
        vocabulary = technique_voc,
        required = True,
        )

    form.fieldset('details', label=_(u"Details"), fields=['body', 'notes'])

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



    # Links fieldset

    form.fieldset('web', label=_(u"Web"), fields=['links'])

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
        self.birthdayYear = self.context.start.year
        self.dimensions = "%d x %d cm" % (self.context.height, self.context.width)
#        self.context.image = self.context.picture # to be able to treat illustration as image in TinyMCE
#        self.context.picture = self.context.image # temporary before I fixed templates
        self.context.description = "%s  %s %s %s %d" % (self.dimensions, self.context.genre, self.context.style, self.context.technique, self.context.start.year)
        
    def mainimage(self):
        """Return image to show in IllustrationFolder view
           Use the following code to call this method from the parent folder: <img tal:define="obj illustration/getObject; image python: obj.restrictedTraverse('@@view').mainimage()"
           [page 182]
        """

        return self.context.image

@form.default_value(field=IIllustration['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

# Works but only the standard message is shown
#@form.validator(field=IIllustration['title'])
#def validateTitle(value):
#    if value and value == value.upper():
#        raise schema.ValidationError(_(u"Please don't shout"))
