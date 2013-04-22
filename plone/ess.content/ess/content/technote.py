from five import grok
from zope import schema
import datetime

from plone.directives import dexterity, form
from plone.app.textfield import RichText

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile


from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from ess.content import _
from collective import dexteritytextindexer

from zope.interface import implements
from zope.interface import Interface

from plone.app.content.interfaces import INameFromTitle

class INameFromDate(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromDate(object):
    implements(INameFromDate)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.start.strftime("%y%m%d")

class ITechreport(form.Schema):
    """
    A short summary about a piece of work
    """

    start = schema.Date(
        title = _(u"Techreport date"),
        description = _(u"Used as its reference ID"),
        )

    # dexteritytextindexer.searchable('description')
    # details = schema.Text(
    #     title = _(u"Abstract1"),
    #     description = _(u"A short summary about this report"),
    #     required = True,
    #     )

    doc = NamedBlobFile(
        title = _(u"Document"),
        description = _(u"File with technical report"),
        required = True,
        )

    attachment = NamedBlobFile(
        title = _(u"Attachment"),
        description = _("Include relevant data, input, source files necessary to understand the report. Multiple files should be added as an archive."),
        required = True,
        )
    
    
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Techreport(dexterity.Item):
    grok.implements(ITechreport)

    # Add your class methods and properties here


class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for tech report
    The associated template is found in techreport_templates/view.pt.
    """

    implements(ITechreport)
    grok.context(ITechreport)
    grok.require('zope2.View')

    def update(self):
        self.startFormatted = self.context.start.strftime("%d %b %Y")
        self.idFormatted = self.context.start.strftime("%y%m%d")


@form.default_value(field=ITechreport['start'])
def startDefaultValue(data):
    return datetime.datetime.today()
