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


# Interface class; used to define content-type schema.

class ITechreport(form.Schema):
    """
    A short summary about a piece of work
    """

    start = schema.Date(
        title = _(u"Techreport date"),
        description = _(u"Used as its reference ID"),
        )

    dexteritytextindexer.searchable('description')
    summary = schema.Text(
        title = _(u"Abstract"),
        description = _(u"A short summary about this report"),
        required = True,
        )

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

class Techreport(dexterity.Container):
    grok.implements(ITechreport)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# Techreport_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(ITechreport)
    grok.require('zope2.View')

    # grok.name('view')

#@form.default_value(field=Techreport['start'])
#def startDefaultValue(data):
#    return datetime.datetime.today()
