from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from kbat.content import _

class IQuote(form.Schema):
    """A quote. Sessions are managed inside Quote Folder.
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        )
    
    
    details = RichText(
        title=_(u"Text"),
        required=False
        )

    title = schema.TextLine(
        title=_(u"Author"),
        )

    url = schema.TextLine(
        title=_(u"Link"),
        )
