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

    ID = schema.ASCIILine(
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
        description = _(u"Use as many lines as necessary"),
        required = False,
        )

    dexteritytextindexer.searchable('mcnp_mt')
    mcnp_mt = schema.ASCIILine(
        title = _(u"MCNP MT"),
        required = False,
        )

    dexteritytextindexer.searchable('mcnp_mx')
    mcnp_mx = schema.ASCII(
        title = _(u"MCNPX MX"),
        description = _(u"Example: ':h model j model'. Use as many lines as necessary."),
        required = False,
        )

    form.fieldset('fluka', label=_(u"FLUKA"), fields=['fluka_string'])
    dexteritytextindexer.searchable('fluka_string')
    fluka_string = schema.ASCII(
        title = _(u"FLUKA string"),
        description = _(u"Use free format."),
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

#    def update(self):
#        print self.mcnp()

    def comments(self):
        """ prints comments before material definition """
        out = "c %s\n" % self.context.title
        out = out + "c %s\n" % self.context.description
        out = out + "c rho = %g g/cm3\n" % self.context.density
        return out

    def mcnp(self):
        """ prints MCNP material definition """
        if not self.context.mcnp_string:
            return "Not defined yet."

        N = 6 # number of spaces between material ID and next number
        N1 = len(self.context.ID) + 1 + 6
        N2 = N - 1 # number of spaces in the MT card (T=1 symbol)
        N3 = N2 - 3 # number of spaces in the MX card (':h' = 2 symbols)
        # comments
        out = self.comments()
        # isotope strings
        out = out + "M%s" % self.context.ID + " "*N
        for i, l in enumerate(self.context.mcnp_string.split('\n')):
            if i==0:
                out = out + l
            else:
                out = out + " "*N1 + l

        if self.context.mcnp_mt:
            out = out + "\n" + "MT" + self.context.ID + " "*N2 + self.context.mcnp_mt

        if self.context.mcnp_mx:
            out = out + "\n"
            for l in self.context.mcnp_mx.split('\n'):
                out = out + "MX" + self.context.ID + l[0:2] + " "*N3 + l[2:]
        return out

    def fluka(self):
        """ prints FLUKA material definition """
        # comments
        if not self.context.fluka_string:
            return "Not defined yet."

        out = self.comments()
        out = out + self.context.fluka_string
        return out
