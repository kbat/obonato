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

from ess.content import _
from collective import dexteritytextindexer

from zope.interface import implements
from zope.interface import Interface

from plone.app.content.interfaces import INameFromTitle
from re import search # for validation

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

class IMinutes(form.Schema):
    """
    A short summary about a piece of work
    """

    start = schema.Date(
        title = _(u"Meeting date"),
#        description = _(u"Used as its reference ID"),
        required = True,
        )

    dexteritytextindexer.searchable('body')
    body = RichText(
        title=_(u"Minutes"),
        required=False,
        )
   
    
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Minutes(dexterity.Item):
    grok.implements(IMinutes)

    # Add your class methods and properties here
#    @property
#    def title(self):
#        return self.start.strftime("%d %b %Y") + "b"

#    def setTitle(self, value):
#        return

class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for tech note
    The associated template is found in minutes_templates/view.pt.
    """

    implements(IMinutes)
    grok.context(IMinutes)
    grok.require('zope2.View')

    def update(self):
        self.startFormatted = self.context.start.strftime("%d %b %Y")
        self.idFormatted = self.context.start.strftime("%y%m%d")
        self.context.title = self.startFormatted


@form.default_value(field=IMinutes['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

# @form.validator(field=IMinutes['doc'])
# def validateDocFilename(value):
#     if not search("\A(1[3-9])(1[0-2]|0[1-9])([012][0-9]|3[01])", value.filename):
#         print value.filename
#         raise schema.ValidationError(u"Minutes file name should start with the date in the format 'yymmdd'");
    
