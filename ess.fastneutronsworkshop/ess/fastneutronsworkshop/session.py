from five import grok
from plone.directives import dexterity, form

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

from ess.fastneutronsworkshop import MessageFactory as _


# Interface class; used to define content-type schema.

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import checkEmailAddress


@grok.provider(IContextSourceBinder)
def possibleRooms(context):
    conference = context.getConference()            
    return SimpleVocabulary.fromValues(conference.rooms)



class ISession(form.Schema, IImageScaleTraversable):
    """
    Conference Session
    """

    form.widget(emails='plone.z3cform.textlines.TextLinesFieldWidget')
    emails = schema.List(title=u"E-mail addresses of speakers", 
        description=u"We will find speakers' profile in the registration " +
                u'using these emails. One in each line', required=True,
                value_type=schema.TextLine())
    title = schema.TextLine(title=u"Session Title")
    description = schema.Text(title=u"Summary", required=True)
    session_type = schema.Choice(
        title=u'Session Type',
        vocabulary="ess.fastneutronsworkshop.vocabulary.sessiontype"
    )
    level = schema.Choice(
        title=u'Level',
        vocabulary="ess.fastneutronsworkshop.vocabulary.sessionlevel"
    )

    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    text = schema.Text(
        title=_(u"More details on proposed session"),
        description=u'',
        required=False,
    )

    attachment = NamedBlobFile(title=u"Attachment",
        description=u"Attach your talks document (slide, code, etc). " + 
                    u"If there are multiple files, include them in a zip " + 
                    u"By uploading the file here, you hereby agreed to " + 
                    u"grants us permission to redistribute this file",
        required=False
    )

    conference_rooms = schema.List(
        title=u'Conference Rooms',
        value_type=schema.Choice(source=possibleRooms),
        required=False
    )

    form.widget(color="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    color = schema.TextLine(
        title=u'Agenda Background Color',
        default=u'3366CC',
        required=False
    )

    form.widget(textColor="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    textColor = schema.TextLine(
        title=u'Agenda Text Color',
        default=u'ffffff',
        required=False
    )

@form.validator(field=ISession['emails'])
def emailsValidator(value):
    for email in value:
        try:
            return checkEmailAddress(email)
        except:
            raise Invalid(u"%s is an invalid email address" % email)



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Session(dexterity.Item):
    grok.implements(ISession)
    grok.provides(ISession)
    
    def owners(self):
        catalog = getToolByName(self, 'portal_catalog')
        return [i.getObject() for i in catalog({
            'path': {
                'query': '/'.join(self.getConference().getPhysicalPath()),
                'depth': 2
            }, 'portal_type': 'ess.fastneutronsworkshop.participant',
            'emails': self.emails
        })]
