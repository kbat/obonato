# -*- coding: utf-8 -*-
from os import path
import re
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
#from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from zope import schema
from zope.interface import implementer
#from collective import dexteritytextindexer
from Products.Five import BrowserView

from cl.content import _


class IComponent(model.Schema):
    """ Marker interface and Dexterity Python Schema for Component
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('component.xml')

    commit = schema.TextLine(
        title=_(u"Commit hash on Git"),
        description=_("The idea is to provide a user the CombLayer version which he can use to build the component using the instructions listed in the 'How to build' field below. Of course the component might be changed in the newer versions and we suppose a user knows this."),
        required = True
    )

    headerURL = schema.URI(
        title=_(u'Header URL'),
        description=_('Link to the class header on GitHub'),
        required=True
    )

    # directives.widget(build=TextLinesFieldWidget)
    build = schema.Text(
        title = _(u"How to build"),
        description = _(u"Instructions how to compile and build the component. It's also a good idea to show how to make the attached POV-Ray image."),
        required = True,
    )

    notes = RichText(
        title=_(u'Notes'),
        description=u'',
        required=False,
    )
    directives.widget('notes', RichTextFieldWidget)
#    model.primary('text')



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

# class View(dexterity.DisplayForm):
#     """ Default view (called @@view) for Component


class View(BrowserView):
    """
    """

    def update(self):
        """ Prepare info for the template """
#        self.commit_url = self.context.commit + " here"

    def commit(self):
        return self.context.commit[:8]

    def commitURL(self):
        return 'https://github.com/sansell/comblayer/commit/' + self.context.commit

    def className(self):
        return path.splitext(self.context.headerURL)[0].split('/')[-1]

    def header(self):
        return self.className() + '.h'

    def cxx(self):
        return self.className() + '.cxx'

    def cxxURL(self):
        incDir = '/'.join(self.context.headerURL.split('/')[:-1])
        return re.sub('Inc', '', incDir) + '/' + self.cxx()
