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


from z3c.relationfield.schema import RelationList, RelationChoice

from kbat.content import _

from zope.interface import implements
from zope.interface import Interface


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
    
    start = schema.Date(
        title = _(u"Date"),
        required = True,
        )

    photo = NamedBlobImage(
        title = _(u"Photo"),
        required = False,
    )

class Plant(dexterity.Item):
    grok.implements(IPlant)
    
class View(grok.View):
    """ Default view @@view """
    implements(IPlant)
    grok.context(IPlant)
    grok.require('zope2.View')
    
    def update(self):
        self.dateFormatted = self.context.start.strftime("%d %b %Y")

@form.default_value(field=IPlant['start'])
def startDefaultValue(data):
    return datetime.datetime.today()
