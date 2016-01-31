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


class IExhibition(form.Schema):
    """An exhibition. Exhibitions are managed inside Exhibition Folder.
    """

    # Main form
    
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )

    location = schema.TextLine(
        title=_(u"Location"),
        required = True
    )

    # description = schema.Text(
    #     title = _(u"Description"),
    #     description = _(u"test of Description"),
    #     required = False,
    #     )

    start = schema.Date(
        title = _(u"Start date"),
        required = True,
        )

    end = schema.Date(
        title = _(u"End date"),
        required = True,
        )

    dexteritytextindexer.searchable('body')
    body = RichText(
        title=_(u"Description"),
        description=_(u"A story about this exhibition"),
        required=False,
        )

    # Links fieldset

    form.fieldset('web', label=_(u"Web"), fields=['links'])

    form.widget(links=TextLinesFieldWidget)
    links = schema.List(
        title = _(u"Links"),
        description = _(u'Various links about this exhibition, one per line'),
        value_type = schema.TextLine(),
        required = False,
        )



# We inherit the View class from dexterity.DisplayForm instead of grok.View in order to be able to show the related items
# as suggested here: http://stackoverflow.com/questions/6920817/rendering-related-items-of-a-dexterity-content-type
class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for a exhibition.
    The associated template is found in exhibition_templates/view.pt.
    """

    implements(IExhibition)
    grok.context(IExhibition)
    grok.require('zope2.View')

    def update(self):
        """Prepare information for the template
        """
        self.startFormatted = self.context.start.strftime("%d %b %Y")
        self.endFormatted = self.context.end.strftime("%d %b %Y")

        self.period = self.startFormatted + " - " + self.endFormatted
        if self.context.start.year == self.context.end.year:
            if self.context.start.month == self.context.end.month:
                self.period = str(self.context.start.day) + " - " + str(self.context.end.day) + " " + self.context.start.strftime("%b") + ", " + str(self.context.start.year)
            else:
                self.period = self.context.start.strftime("%d %b") + " - " + self.context.end.strftime("%d %b") + ", " + str(self.context.start.year)
        
        body = ""
        if self.context.body:
            body = self.context.body.output
        self.context.description = "%s, %s" % (self.context.location, self.period)

    def images(self):
        """Return catalog search results of images to show
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides="Products.ATContentTypes.interfaces.image.IATImage",
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='getObjPositionInParent')

        
@form.default_value(field=IExhibition['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

@form.default_value(field=IExhibition['end'])
def endDefaultValue(data):
    return datetime.datetime.today()
