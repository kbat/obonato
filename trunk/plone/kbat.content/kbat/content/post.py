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
from plone.app.content.interfaces import INameFromTitle
from plone.memoize.instance import memoize
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName


from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from kbat.content import _

class INameFromDate(INameFromTitle):
    def title():
        """Return a processed title"""
        
class NameFromDate(object):
    grok.implements(INameFromDate)

    def __init__(self, context):
        print "NameFromDate: init called"
        self.context = context

    @property
    def title(self):
        print "NameFromDate: title property set"
        return u"custom title" #self.context.start.strftime("%y%m%d")


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

    title = schema.TextLine(
        title = _(u"Title"),
        required = True,
        )
    
    start = schema.Date(
        title = _(u"Date of the post"),
        required = True,
        )
    
    details = RichText(
        title=_(u"Text"),
        required=False
        )

    private_notes = RichText(
        title=_(u"Private notes"),
        required=False
        )

    form.fieldset('weather', label=_(u"Weather"), fields=['tinside', 'toutside', 'humidity', 'pressure', 'weather'])
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

    pressure = schema.Int(
        title=_(u"Pressure"),
        description=_(u"in mm"),
        required=False,
        )

    weather = schema.Text(
        title = _(u"Weather notes"),
        description = _(u"Other notes about the weather"),
        required = False,
        )



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Post(dexterity.Container):
    """Customised Post content class"""
    grok.implements(IPost)
    
    # Add your class methods and properties here
    # @property
    # def title(self):
    #     print "Post: title property set"
    #     if hasattr(self, 'start'):
    #         print "has start attribute"
    #         return "generated-title"

    # def defTitle(self, value):
    #     print "Post: setTitle called"
    #     return "aa"

# see davidjb.com/blog/2010/04/plone-and-dexterity-working-with-computed-fields for explanation why setTitle is needed

# View class
# The view will automatically use a similarly named template in
# post_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IPost)
    grok.require('zope2.View')
    
    # grok.name('view')

    def update(self):
        self.dateFormatted = self.context.start.strftime("%d %b %Y")

    @memoize # [page 259]
    def images(self):
        """Return catalog search results of images to show
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides="Products.ATContentTypes.interfaces.image.IATImage",
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='getObjPositionInParent',
                       )

    def imagesLimited(self):
        """Return catalog search results of images to show limited by context.nimages
        """
        images = self.images()
        return images
        # if self.context.nimages < 0:
        #     return images
        # else:
        #     return images[:self.context.nimages]




@form.default_value(field=IPost['start'])
def startDefaultValue(data):
    return datetime.datetime.today()

# why does not work?
@form.validator(field=IPost['humidity'])
def validateHumidity(value):
    if value and value > 100:
        raise schema.ValidationError(u"Humidity is relative: 0 - 100%")
