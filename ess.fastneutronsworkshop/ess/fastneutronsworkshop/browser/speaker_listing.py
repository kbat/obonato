from five import grok
from ess.fastneutronsworkshop.conference import IConference
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class SpeakerListView(grok.View):
    grok.context(IConference)
    grok.template('speaker_listing')
    grok.name('speakers')
    grok.require('zope2.View')

    title = u"Speakers"

    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'ess.fastneutronsworkshop.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'sortable_title'
        })
        return [i.getObject() for i in brains if self._has_session(i)]

    def _has_session(self, brain):
        catalog = getToolByName(self.context, 'portal_catalog')
        return len(catalog({
            'portal_type': 'ess.fastneutronsworkshop.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'emails': brain.emails
        })) > 0
