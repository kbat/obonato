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
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFCore.utils import getToolByName

from ess.fastneutronsworkshop import MessageFactory as _

import datetime

# Interface class; used to define content-type schema.

class IParticipant(form.Schema, IImageScaleTraversable):
    """
    Conference Participant
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/participant.xml to define the content type
    # and add directives here as necessary.
    title = schema.TextLine(title=u"Name",
            required=True)

    description = schema.Text(
        title=u"Description",
#        description=(u"Tell us more about yourself"),
        required=False,
    )

    email = schema.TextLine(
        title=u"E-mail",
        required=True,
    )

    # phone = schema.TextLine(
    #     title=u"Phone number",
    #     required=False
    # )



    organization = schema.TextLine(
        title=u"Affiliation",
        required=True,
    )

    poster_title = schema.TextLine(
        title=u"Poster title",
        description=u"If you want to present a poster, please specify its title",
        required=False,
        )

    poster_abstract = schema.Text(
        title=u'Poster abstract',
        description=u"If you want to present a poster, please specify its abstract",
        required=False
    )

    date_arrive = schema.Date(
        title = _(u"Arrival"),
        required = True,
        )

    date_departure = schema.Date(
        title = _(u"Departure"),
        required = True,
        )

    # need_accommodation = schema.Bool(
    #         title=u'Accommodation',
    #         description=u'Mark here if you need accommodation', required=False)

    # room_size = schema.Choice(
    #     title=u"Room size",
    #     vocabulary="ess.fastneutronsworkshop.vocabulary.roomsize",
    #     required=False
    # )


    # country = schema.Choice(
    #     title=u"Country",
    #     description=u"Where you are from",
    #     required=False,
    #     vocabulary="ess.fastneutronsworkshop.vocabulary.countries"
    # )





    # photo = NamedBlobImage(
    #     title=u"Photo",
    #     description=u"Your photo or avatar. Recommended size is 150x195",
    #     required=False
    #     )

    # form.fieldset('sponsorship',
    #         label=u"Funding",
    #         fields=['need_sponsorship', 'roomshare', 'comment']
    # )


    # roomshare = schema.Bool(
    #         title=u'Roomshare',
    #         description=u'If you want or need a room, check this option',
    #         required=False)

    comment = schema.Text(
        title=u'Comments',
        description=u'''Fill in this field with things you need the organizers
        to know. If you are roomsharing and already have a roommate, please
        mention your roommate's name here''',
        required=False
    )

    # form.widget(color="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    # color = schema.TextLine(
    #     title=u'Person Color Tag',
    #     default=u'cccccc',
    #     required=False
    # )




# @form.validator(field=IParticipant['photo'])
# def maxPhotoSize(value):
#     if value is not None:
#         if value.getSize()/1024 > 512:
#             raise schema.ValidationError(u"Please upload image smaller than 512KB")



@form.validator(field=IParticipant['email'])
def emailValidator(value):
    try:
        return checkEmailAddress(value)
    except:
        raise Invalid(u"Invalid email address")

# @form.validator(field=IParticipant['is_poster'], )
# def is_posterValidator(value):
#     print value, self.context.poster_title
#     if value and not self.context.poster_title:
#         raise Invalid(u"wrong is_poster")



class Participant(dexterity.Item):
    grok.implements(IParticipant)
    grok.provides(IParticipant)


    def sessions(self):
        catalog = getToolByName(self, 'portal_catalog')
        result =  catalog({
            'path': {
                'query': '/'.join(self.getConference().getPhysicalPath()),
                'depth': 2
            }, 'portal_type': 'ess.fastneutronsworkshop.session',
            'emails': self.email
        })
        return [i.getObject() for i in result]

@form.default_value(field=IParticipant['date_arrive'])
def date_arriveDefaultValue(data):
    return datetime.datetime(2013, 9, 30)

@form.default_value(field=IParticipant['date_departure'])
def date_departureDefaultValue(data):
    return datetime.datetime(2013, 10, 1)
