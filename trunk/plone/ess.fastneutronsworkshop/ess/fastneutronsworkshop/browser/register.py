from five import grok
from ess.fastneutronsworkshop.participant import IParticipant, Participant
from ess.fastneutronsworkshop.conference import IConference
#from plone.formwidget.captcha import CaptchaFieldWidget
#from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.error import ErrorViewSnippet

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage

class IRegistrationForm(IParticipant):

    publishinfo = schema.Bool(
        title=u"Show me in attendee list",
        description=u"Check this if you wish your name and contact info" +
                    " to be published in our attendee listing",
        required=False
    )

#    form.widget(captcha=CaptchaFieldWidget)
#    captcha = schema.TextLine(title=u"",  required=False)

#    form.omitted('color')
    form.omitted('description') # hide this field
#    form.omitted('photo')
    form.omitted('publishinfo')

# @form.validator(field=IRegistrationForm['captcha'])
# def validateCaptca(value):
#     site = getSite()
#     request = getRequest()
#     if request.getURL().endswith('kss_z3cform_inline_validation'):
#         return

#     captcha = CaptchaValidator(site, request, None,
#             IRegistrationForm['captcha'], None)
#     captcha.validate(value)


class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IConference)
    grok.require("zope.Public")
    schema = IRegistrationForm
    label = u"Register for this event"


    def create(self, data):
        inc = getattr(self.context, 'registrant_increment', 0) + 1
        data['id'] = 'participant-%s' % inc
        self.context.registrant_increment = inc
        obj = _createObjectByType("ess.fastneutronsworkshop.participant", 
                self.context, data['id'])

#        publishinfo = data['publishinfo']
#        del data['captcha']
#        del data['publishinfo']
        for k, v in data.items():
            setattr(obj, k, v)

        portal_workflow = getToolByName(self.context, 'portal_workflow')
        # if publishinfo:
        #     portal_workflow.doActionFor(obj, 'anon_publish')
        # else:
        portal_workflow.doActionFor(obj, 'anon_hide')
        obj.reindexObject()

# email form
        variables = {'sender_from_address': "kbat@mail.ru",
                     'sender_fullname' : "Konstantin",
                     'url' : 'http://plone.esss.lu.se/fast-neutrons-workshop',
                     'subject' : 'workshop registration',
                     'affiliation' : 'ESS',
                     'message' : 'etotest'}

        message = self.context.site_feedback_template(self.context, **variables)
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        encoding = portal.getProperty('email_charset')
        message = message.encode(encoding)
        host = self.context.MailHost
        result = host.send(message, 'kbat@yandex.ru', 'kbat@yandex.ru', subject='workshop registration', charset=encoding)

        IStatusMessage(self.request).addStatusMessage(
            'Thank you. You are now registered.'
        )
        return obj

    def add(self, obj):
        pass
