from five import grok
from ess.fastneutronsworkshop.conference import IConference
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class SessionListView(grok.View):
    grok.context(IConference)
    grok.template('session_listing')
    grok.name('sessions')

    title = u"Sessions"

    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'ess.fastneutronsworkshop.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'sortable_title'
        })
        objs = [i.getObject() for i in brains]
        return [i for i in objs if (i.session_type != 'Meta')]
