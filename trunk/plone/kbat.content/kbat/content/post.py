from five import grok
from plone.directives import dexterity, form
import datetime

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from kbat.content import _


# Interface class; used to define content-type schema.

class IPost(form.Schema, IImageScaleTraversable):
    """
    Post of the Blog
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/post.xml to define the content type
    # and add directives here as necessary.

    start = schema.Date(
        title = _(u"Date of the post"),
        required = True,
        )
    
    details = RichText(
        title=_(u"Text"),
        required=False
        )

    form.fieldset('weather', label=_(u"Weather"), fields=['tinside', 'toutside', 'humidity', 'weather'])
    tinside = schema.Int(
        title=_(u"Inside temperature"),
        description=_(u"in deg C"),
        required=False,
        )

    toutside = schema.Int(
        title=_(u"Outside temperature"),
        description=_(u"in deg C"),
        required=False,
        )

    humidity = schema.Int(
        title=_(u"Inside humidity"),
        description=_(u"in %"),
        required=False,
        )

    weather = schema.Text(
        title = _(u"Weather notes"),
        description = _(u"Other notes about the weather"),
        required = False,
        )




# why does not work?
@form.validator(field=IPost['humidity'])
def validateHumidity(value):
    if value and value > 100:
        raise schema.ValidationError(u"Humidity is relative: 0 - 100%")

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Post(dexterity.Container):
    grok.implements(IPost)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# post_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(IPost)
    grok.require('zope2.View')
    
    # grok.name('view')

    def update(self):
        self.dateFormatted = self.context.start.strftime("%d %b %Y")


@form.default_value(field=IPost['start'])
def startDefaultValue(data):
    return datetime.datetime.today()
