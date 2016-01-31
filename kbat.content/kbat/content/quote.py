from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from kbat.content import _

class IQuote(form.Schema):
    """A quote. Quotes are managed inside Quote Folder.
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
    grok.context(IQuote)
    grok.require('zope2.View')
