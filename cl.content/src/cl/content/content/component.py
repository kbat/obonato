# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
#from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from zope import schema
from zope.interface import implementer
#from collective import dexteritytextindexer

from cl.content import _


class IComponent(model.Schema):
    """ Marker interface and Dexterity Python Schema for Component
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('component.xml')

    commit = schema.TextLine(
        title=_(u"Commit hash on GitHub"),
        required = True
    )

    header = schema.URI(
        title=_(u'Header'),
        description=_('URL to the class header on GitHub'),
        required=True
    )

    # directives.widget(build=TextLinesFieldWidget)
    # build = schema.List(
    #     title = _(u"How to build"),
    #     description = _(u"Instructions how to build the component"),
    #     value_type = schema.TextLine(),
    #     required = True,
    #     )


#    fieldset('Miscellaneous', fields=['text'])
#    dexteritytextindexer.searchable('text')
    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IComponent)
class Component(Item):
    """
    """
