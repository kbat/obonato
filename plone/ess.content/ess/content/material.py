from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from ess.content import _
#MessageFactory as _

from collective import dexteritytextindexer

from zope.interface import implements
from zope.interface import Interface

from plone.app.content.interfaces import INameFromTitle
from re import search # for validation

class INameFromID(INameFromTitle):
    def title():
        """Return a processed material ID"""

class NameFromID(object):
    implements(INameFromID)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.ID


# Interface class; used to define content-type schema.

class IMaterial(form.Schema):
    """
    Material for Monte Carlo studies
    """

    # title = schema.TextLine(
    #     title=_(u"Title"),
    #     required = True
    #     )

    ID = schema.ASCII(
        title = _(u"Material ID"),
        required = True,
        )

    density = schema.Float(
        title = _(u"Material density [g/cm3]"),
        required = True,
        )

    form.fieldset('mcnp', label=_(u"MCNP"), fields=['mcnp_string', 'mcnp_mt', 'mcnp_mx'])

    dexteritytextindexer.searchable('mcnp_string')
    mcnp_string = schema.ASCII(
        title = _(u"MCNP string"),
        required = False,
        )

    dexteritytextindexer.searchable('mcnp_mt')
    mcnp_mt = schema.ASCIILine(
        title = _(u"MCNP MT"),
        required = False,
        )

    dexteritytextindexer.searchable('mcnp_mx')
    mcnp_mx = schema.ASCIILine(
        title = _(u"MCNPX MX"),
        required = False,
        )

    form.fieldset('fluka', label=_(u"FLUKA"), fields=['fluka_string'])
    dexteritytextindexer.searchable('fluka_string')
    fluka_string = schema.ASCII(
        title = _(u"FLUKA string"),
        required = False,
        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Material(Container):
    grok.implements(IMaterial)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# material_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(IMaterial)
    grok.require('zope2.View')

    def update(self):
        print "M%s     " % self.context.ID,
        for i, l in enumerate(self.context.mcnp_string.split('\n')):
            if i==0:
                print l
            else:
                print " "*11, l
