from five import grok
from plone.directives import dexterity, form
import datetime

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer

from plone.app.textfield import RichText
from plone.memoize.instance import memoize
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from kbat.content import _

from zope.interface import implements
from zope.interface import Interface

lighting_voc = SimpleVocabulary(
    [ SimpleTerm(value=u'full_light', title=_(u'full_light', default='Full light')),
      SimpleTerm(value=u'prenumbra', title=_(u'prenumbra', default='Prenumbra')),
      SimpleTerm(value=u'shadow', title=_(u'shadow', default='Shadow')) ])

stratification_voc = SimpleVocabulary(
    [ SimpleTerm(value=u'required', title=_(u'required', default='Required')),
      SimpleTerm(value=u'desirable', title=_(u'desirable', default='Desirable')),
      SimpleTerm(value=u'unnecessary', title=_(u'unnecessary', default='Unnecessary')) ])

vitality_voc = SimpleVocabulary(
    [ SimpleTerm(value=u'ot', title=_(u'ot', default='Highly termophilic')),
      SimpleTerm(value=u't', title=_(u't', default='Termophilic')),
      SimpleTerm(value=u'uv', title=_(u'uv', default='Moderately cold resistant')),
      SimpleTerm(value=u'v', title=_(u'v', default='Cold resistant')),
      SimpleTerm(value=u'ov', title=_(u'ov', default='Highly cold resistant')) ])

# Interface class; used to define content-type schema.

class IPlant(form.Schema):
    """
    A plant in the garden
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/plant.xml to define the content type
    # and add directives here as necessary.

    latin = schema.TextLine(
        title = _(u"latin_name", default=u"Latin name"),
        required = True)

    dexteritytextindexer.searchable('body')
    body = RichText(
        title = _(u"notes", default=u"Notes"),
        required = False)

    lighting = schema.Choice(
        title = _(u"lighting", default=u"Lighting"),
        vocabulary = lighting_voc,
        required = False)

    allelopathic = RelationList(
        title = _(u"Allelopathic plants", default=u"Allelopathic plants"),
        default = [],
# TODO: this is ugly since depends on absolute path:
        value_type=RelationChoice(title=_(u"Related"),
#                                  source=ObjPathSourceBinder(navigation_tree_query={'path':{'query':'/kbat/test/rasteniya'},
#                                                                                    'object_provides':'kbat.content.plant'})),
                                  source=ObjPathSourceBinder(navigation_tree_query={'path':{'query':'/kbat/test/rasteniya'} })),
        required = False)

    photo = NamedBlobImage(
        title = _(u"photo", default=u"Photo"),
        required = False)

    form.fieldset('seeds',
                  label=_(u"Seeds"),
                  fields=['seed_storage_period',
                          'seed_density',
                          'seed_demand',
                          'seed_stratification',
                          'seed_depth',
                          'seed_min_distance',
                          'seed_row',
                          'seed_tmin',
                          'seed_vitality',
                          'seed_shoots'])

    seed_storage_period = schema.Float(
        title=_(u"seed_storage_period", default="Storage period"),
        required = False)

    seed_density = schema.Int(
        title=_(u"seed_density", default="Number of seeds in 5 g"),
        required = False)

    seed_demand = schema.TextLine(
        title=_(u"seed_demand", default="Number of seeds per a 10 m long row"),
        required = False)

    seed_stratification = schema.Choice(
        title = _(u"stratification", default="Stratification"),
        vocabulary = stratification_voc,
        required = False)

    seed_depth = schema.Float(
        title = _(u"seed_depth", default="Seeding depth"),
        required = False)

    seed_min_distance = schema.TextLine(
        title = _(u"seed_min_distance", default="Minimal distance in a row"),
        description = _(u"[cm]"),
        required = False)

    seed_row = schema.TextLine(
        title = _(u"seed_row", default="Distance between rows"),
        description = _(u"[cm]"),
        required = False)

    seed_tmin = schema.Int(
        title=_(u"seed_tmin", default="Minimal soil temperature [deg C]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    seed_vitality = schema.Choice(
        title = _(u"vitality", default="Cold resistance"),
        vocabulary = vitality_voc,
        required = False)

    seed_shoots = schema.TextLine(
        title = _(u"seed_shoots", default="Shoots [days]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    form.fieldset('sprout', label=_(u"Sprouts"),
                  fields=['sprout_depth',
                          'sprout_min_distance',
                          'sprout_temp',
                          'sprout_shoots',
                          'sprout_age',
                          'sprout_min_distance_bed',
                          'sprout_tmin_bed',
                          'sprout_vitality',
                          'sprout_notes'])

    sprout_depth = schema.Float(
        title = _(u"sprout_depth", default="Sprout seeding depth [cm]"),
        required = False)

    sprout_min_distance = schema.Float(
        title = _(u"sprout_min_distance", default="Minimal distance between plants [cm]"),
        required = False)

    sprout_temp = schema.TextLine(
        title = _(u"sprout_temp", default="Soil temperature range [deg C]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    sprout_shoots = schema.TextLine(
        title = _(u"sprout_shoots", default="Shoots [days]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    sprout_age = schema.TextLine(
        title = _(u"sprout_age", default="Optimal sprout age when seeding [weeks]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    sprout_min_distance_bed = schema.Float(
        title = _(u"sprout_min_distance_bed", default="Minimal distance in the bed [cm]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    sprout_tmin_bed = schema.Int(
        title = _(u"sprout_tmin_bed", default="Minimal temperature in the bed [deg C]"),
        description=_(u"TODO: add description from the book"),
        required = False)

    sprout_vitality = schema.Choice(
        title = _(u"vitality", default="Cold resistance"),
        vocabulary = vitality_voc,
        required = False)

    sprout_notes = schema.Text(
        title = _(u"notes", default="Notes on sprouts"),
        required = False)

class Plant(dexterity.Item):
    grok.implements(IPlant)

class View(grok.View):
    """ Default view @@view """
    implements(IPlant)
    grok.context(IPlant)
    grok.require('zope2.View')

    def seedPreTable(self):
        """ Checks if pre-sowing properties of seeds contain any info """
        return self.context.seed_storage_period or self.context.seed_density or self.context.seed_demand or self.context.seed_stratification

    def seedSowTable(self):
        """ Checks if seed sowing properties contain any info """
        return  self.context.seed_depth or self.context.seed_min_distance or self.context.seed_row or self.context.seed_tmin or self.context.seed_vitality or self.context.seed_shoots

    def sproutTable(self):
        """ Checks is the sproud table has any info """
        return self.context.sprout_depth or self.context.sprout_min_distance or self.context.sprout_temp or self.context.sprout_shoots or self.context.sprout_age or self.context.sprout_min_distance_bed or self.context.sprout_tmin_bed or self.context.sprout_vitality

#    def update(self):
#        self.dateFormatted = self.context.start.strftime("%d %b %Y")
