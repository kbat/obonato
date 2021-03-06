from five import grok

from z3c.form import group, field, validator
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
import re
import textwrap

# ID validation
from plone import api
from zope.lifecycleevent.interfaces import IObjectModifiedEvent #IObjectCreatedEvent, IObjectAddedEvent
#from Products.CMFCore.interfaces import IContentish # a non-folderish object
from plone.supermodel import model


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


def MXConstraint(value):
    """ checks the mcnp_mx field """
    for l in value.split('\n'):
        if l[0] != ':':
            raise Invalid("Line '%s' is wrong." % l)
    return True

def MCNPStringConstraint(value):
    """ checks the mcnp_string field. TODO: add possibility to include nlib, pnlib and plib, see Manual 3-122 """
    lines = value.split('\n')
    nlines = len(lines)
    for i,l in enumerate(lines):
        w = l.strip().split()
        if not len(w):
            raise Invalid("Material definition should not contain empty lines")
        if i!=nlines-1:
            if len(w) != 2:
                raise Invalid("Number of records in the line '%s' is wrong." % l)
            if not re.search("\..", w[0]):
                raise Invalid("Library identifier is not specified in the entry '%s' of the line '%s'" % (w[0], l))
            try:
                a = float(w[1])
            except ValueError:
                raise Invalid("Entry '%s' in the line '%s' must be a float number." % (w[1], l))
            else:
                pass
#        if not isinstance(w[1], float):
#            print "here: _%s_" % w[1]
#            raise Invalid("Second entry %s in the line '%s' must be a float number." % (w[1], l))
    return True


#class MCNPStringMT(Invalid):
#    __doc__ = _(u"MCNP string and MT record do not match.")

# Interface class; used to define content-type schema.

class IMaterial(form.Schema):
    """
    Material for Monte Carlo studies
    """

    # title = schema.TextLine(
    #     title=_(u"Title"),
    #     required = True
    #     )

#    theid = schema.Id(
#        title = _("id"),
#        )

    ID = schema.ASCIILine(
        title = _(u"Material ID"),
        description = _(u"Use 8 or less digits."),
        required = True,
        )

    density = schema.Float(
        title = _(u"Material density [g/cm3]"),
        description = _("A float number with max 3 digits after the point."),
        required = True,
        min = 0.0,
        )

    temperature = schema.Float(
        title = _(u"Material temperature [K]"),
        required = False,
        min = 0.0,
        )

    dexteritytextindexer.searchable('reference')
    reference = schema.ASCII(
        title = _(u"Reference"),
        description = _(u"Specify the sources of information about this material."),
        required = True,
        )

    form.fieldset('mcnp', label=_(u"MCNP"), fields=['mcnp_string', 'mcnp_mt', 'mcnp_mx'])

    dexteritytextindexer.searchable('mcnp_string')
    mcnp_string = schema.ASCII(
        title = _(u"M card"),
        description = _(u"Use as many lines as necessary. Each line should contain only 2 entries: isotope id and its atomic fraction. Last line may contain material card keywords."),
        required = False,
        constraint = MCNPStringConstraint,
        )

    dexteritytextindexer.searchable('mcnp_mt')
    mcnp_mt = schema.ASCIILine(
        title = _(u"MT card"),
        required = False,
        )

    dexteritytextindexer.searchable('mcnp_mx')
    mcnp_mx = schema.ASCII(
        title = _(u"MX card"),
        description = _(u"Use as many lines as necessary. Each MX record should start with colon followed by a particle ID. Example: ':h model j model'."),
        required = False,
        constraint = MXConstraint,
        )


    form.fieldset('fluka', label=_(u"FLUKA"), fields=['fluka_string'])
    dexteritytextindexer.searchable('fluka_string')
    fluka_string = schema.ASCII(
        title = _(u"FLUKA string"),
        description = _(u"Use free format."),
        required = False,
        )

    # does not work with 2 filed sets (MCNPX and FLUKA)
    # @invariant
    # def validateMCNPStringMT(data):
    #     """ checks whether number of entries in the MT record is > than the lines in the MCNP string """
    #     nmt = len(data.mcnp_mt.split())
    #     nstring = len(data.mcnp_string.split('\n'))
    #     if nstring < nmt:
    #         raise MCNPStringMT("The MT record contains more records (%d) than number of lines in the MCNP string (%d)." % (nmt, nstring))
    #     return True


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Material(Container):
    grok.implements(IMaterial)
    isAdded = False # true if this object already exists

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

    def comments(self, code="MCNP"):
        """ prints comments before material definition """
        comsign = "c "
        if code == "CombLayer":
            comsign = "// "

        out = comsign + "%s\n" % self.context.title
        out += comsign + "%s\n" % textwrap.fill(self.context.description, width=75, subsequent_indent=comsign)
        if code != "CombLayer":
            out += comsign + "Density:    %g g/cm3\n" % self.context.density
        if self.context.temperature is not None: out += comsign + "Temperature: %g K\n" % self.context.temperature
        if self.context.reference is not None:
            out += comsign + "Reference: "
            out += "%s\n" % textwrap.fill(self.context.reference, width=75, subsequent_indent=comsign)

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
        out = self.comments("MCNP")
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

        out = self.comments("FLUKA")
        out = out + self.context.fluka_string
        return out

    def CombLayer(self):
        """ prints CombLayer material definition """
        if not self.context.mcnp_string:
            return "Not defined yet."

        clID = re.sub('^0+', '', self.context.ID)
        out = self.comments("CombLayer")
        out += "MObj.setMaterial(%s, \"M%s\",\n" % (clID, self.context.ID)
        for l in self.context.mcnp_string.split('\n'):
            out += " "*17 + "\" " + l.strip() + " \"\n"
        out = out.strip()
        out += ", \"%s\", MLib);\n" % (self.context.mcnp_mt or "") # same as ('' if self.context.mcnp_mt is None else str(self.context.mcnp_mt))
        if self.context.mcnp_mx:
            for i,l in enumerate(self.context.mcnp_string.split('\n')):
                w = l.strip().split()
                nuclide = w[0].split('.')
                for p in self.context.mcnp_mx.split('\n'):
                    out += "MObj.setMXitem(%s, %s, '%s', '%s');\n" % (nuclide[0], nuclide[1][0:-1], nuclide[1][-1], p[1])
        out += "MObj.setDensity(%g);\n" % -self.context.density
        out += "MDB.resetMaterial(MObj);\n"
        return out


class IDValidator(validator.SimpleFieldValidator):
    """ checks whether ID is valid """
    def validate(self, value):
        super(IDValidator, self).validate(value)

        if not value.isdigit():
            raise Invalid("Material ID must contain only digits.")
        if len(value)>8:
            raise Invalid("Material ID is too long. It should contain 8 or less digits.")

        md = api.content.get(path='/eval/docs/neutronics/materials/database') or api.content.get(path='/Plone/materials/')
        for key,val in md.items():
            if key == value and val != self.context:
                raise Invalid("Material with ID %s already exists" % value)


validator.WidgetValidatorDiscriminators(IDValidator, field=IMaterial['ID'])
grok.global_adapter(IDValidator)

# rename material if ID was changed (actually, the INameFromID is not needed with this function):
# this method is called after View::update()
@grok.subscribe(IMaterial, IObjectModifiedEvent)
def rename(obj, event):
    oldid = obj.getId()
    newid = obj.ID
    if oldid != newid:
        parent = obj.aq_parent
        parent.manage_renameObject(oldid, newid)
