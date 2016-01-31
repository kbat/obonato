from five import grok

from ess.fastneutronsworkshop.conference import IConference

grok.templatedir('templates')

class ConferenceView(grok.View):
    grok.context(IConference)
    grok.name('view')
    grok.template('conference_view')
    grok.require('zope2.View')
