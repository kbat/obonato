from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

class IQuoteFolder(form.Schema):
    """A quote folder.
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        )
    
    
    details = RichText(
        title=_(u"Text"),
        required=False
        )

