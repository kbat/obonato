from plone.indexer.decorator import indexer
from ess.fastneutronsworkshop.conference import IConference
from ess.fastneutronsworkshop.session import ISession
from ess.fastneutronsworkshop.participant import IParticipant


@indexer(IConference)
def c_conference_rooms(obj, **kw):
    return obj.rooms

@indexer(ISession)
def s_conference_rooms(obj, **kw):
    return obj.conference_rooms

@indexer(IParticipant)
def p_emails(obj, **kw):
    return [obj.email]
