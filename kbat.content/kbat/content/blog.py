from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid, alsoProvides
try:
    # plone 4
    from zope.app.content.interfaces import IContentType
except ImportError:
    # plone 5
    from plone.dexterity.interfaces import IContentType

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
#from plone.formwidget.contenttree import ObjPathSourceBinder

from kbat.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IBlog(form.Schema):
    """
    Blog - a folder for Posts
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/blog.xml to define the content type
    # and add directives here as necessary.
 

#    form.model("models/blog.xml")
#alsoProvides(IBlog, IContentType)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Blog(dexterity.Container):
    grok.implements(IBlog)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# blog_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(IBlog)
    grok.require('zope2.View')
    
    # grok.name('view')
