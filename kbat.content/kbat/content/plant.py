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
    [ SimpleTerm(value=u'none', title=_(u'-')),
      SimpleTerm(value=u'sun', title=_(u'Full light')),
      SimpleTerm(value=u'prenumbra', title=_(u'Prenumbra')),
      SimpleTerm(value=u'shadow', title=_(u'Shadow')) ]
    )

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
    
    lighting = schema.Choice(
        title = _(u"Lighting"),
        vocabulary = lighting_voc,
        required = False,
        )

    allelopathic = RelationList(
        title = _(u"Allelopathic plants"),
        default = [],
# TODO: this is ugly since depends on absolute path:
        value_type=RelationChoice(title=_(u"Related"),
#                                  source=ObjPathSourceBinder(navigation_tree_query={'path':{'query':'/kbat/test/rasteniya'},
#                                                                                    'object_provides':'kbat.content.plant'})),
                                  source=ObjPathSourceBinder(navigation_tree_query={'path':{'query':'/kbat/test/rasteniya'} })),
        required = False,
        )

    photo = NamedBlobImage(
        title = _(u"Photo"),
        required = False,
    )

    form.fieldset('seeding', label=_(u"Seeding"), fields=['seeding_notes'])

    seeding_notes = schema.Text(
        title = _(u"Notes"),
        description = _(u"Seeding notes"),
        required = False)

class Plant(dexterity.Item):
    grok.implements(IPlant)
    
class View(grok.View):
    """ Default view @@view """
    implements(IPlant)
    grok.context(IPlant)
    grok.require('zope2.View')
    
#    def update(self):
#        self.dateFormatted = self.context.start.strftime("%d %b %Y")
