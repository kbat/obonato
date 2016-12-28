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

class ITechnote(form.Schema):
    """
    A short summary about a piece of work
    """

    start = schema.Date(
        title = _(u"Release date"),
        description = _(u"Used as its reference ID"),
        required = True,
        )

    # dexteritytextindexer.searchable('description')
    # details = schema.Text(
    #     title = _(u"Abstract1"),
    #     description = _(u"A short summary about this note"),
    #     required = True,
    #     )

    dexteritytextindexer.searchable('doc')
    doc = NamedBlobFile(
        title = _(u"Document"),
        description = _(u"File with technical note. The file name will be prefixed with the technote id of the form 'yymmdd' if not already done so."),
        required = True,
#        validator = validateDocFilename(),
        )

    dexteritytextindexer.searchable('attachment')
    attachment = NamedBlobFile(
        title = _(u"Attachment"),
        description = _("Include relevant data, input, source files necessary to understand the note. Multiple files should be added as an archive. The file name will be prefixed with the technote id of the form 'yymmdd' if not already done so."),
        required = True,
        )
    
    
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Technote(dexterity.Item):
    grok.implements(ITechnote)

    # Add your class methods and properties here


class View(dexterity.DisplayForm):
    """Default view (called "@@view"") for tech note
    The associated template is found in technote_templates/view.pt.
    """

    implements(ITechnote)
    grok.context(ITechnote)
    grok.require('zope2.View')

    def update(self):
        self.startFormatted = self.context.start.strftime("%d %b %Y")
        self.idFormatted = self.context.start.strftime("%y%m%d")
        # check if the prefix is the date in the form yymmdd:
        if not search("\A([0-9][0-9])(1[0-2]|0[1-9])([012][0-9]|3[01])", self.context.doc.filename):
            self.context.doc.filename = _(u"%s-%s" % (self.idFormatted, self.context.doc.filename))
        if self.context.attachment and not search("\A([0-9][0-9])(1[0-2]|0[1-9])([012][0-9]|3[01])", self.context.attachment.filename):
            self.context.attachment.filename = _(u"%s-%s" % (self.idFormatted, self.context.attachment.filename))


@form.default_value(field=ITechnote['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

# @form.validator(field=ITechnote['doc'])
# def validateDocFilename(value):
#     if not search("\A(1[3-9])(1[0-2]|0[1-9])([012][0-9]|3[01])", value.filename):
#         print value.filename
#         raise schema.ValidationError(u"Technote file name should start with the date in the format 'yymmdd'");
    
