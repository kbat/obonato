from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from lizardie.content import _

class IDoll(form.Schema):
    """A doll. Dolls are managed inside Doll Folder.
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        required = True
        )
    
    text = RichText(
        title=_(u"Text"),
        required=True
        )

    author = schema.TextLine(
        title=_(u"Author"),
        required = False
        )

    url = schema.TextLine(
        title=_(u"Link"),
        description=_(u"URL must start with protocol name"),
        required = False
        )

class View(grok.View):
    grok.context(IDoll)
    grok.require('zope2.View')
