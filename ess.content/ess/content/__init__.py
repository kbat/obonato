from zope.i18nmessageid import MessageFactory
contentMessageFactory = MessageFactory('ess.content')

_ = MessageFactory("ess.content")

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
