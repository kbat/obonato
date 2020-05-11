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
from zope.interface import Invalid
import urllib

from cl.content import _

origin = 'https://github.com/sansell/comblayer'

def url_is_alive(url):
    """Checks that a given URL is reachable.
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

def headerURL_constraint(value):
    """Check that the headerURL is OK
    """
    if not value.endswith('.h'):
        raise Invalid(_(u"Header file extension must end with .h"))
    if not value.lower().startswith(origin+'/'):
        raise Invalid(_(u'URL must start with %s' % origin))

    ### this sends too many requests -> commenting out
    # response = urllib.urlopen(value)
    # code = response.getcode()
    # response.close()
    # if code == 404:
    #     raise Invalid(_(u'Address is not reachable'))

    return True

class IComponent(model.Schema):
    """ Marker interface and Dexterity Python Schema for Component
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('component.xml')

    commit = schema.TextLine(
        title=_(u"Commit hash on Git"),
        description=_("The idea is to provide a user the CombLayer version which he can use to build the component using the instructions listed in the 'How to build' field below. Of course the component might be changed in the newer versions and we suppose a user knows this."),
        min_length=7,
        max_length=40,
        required = True
    )

    headerURL = schema.URI(
        title=_(u'Header URL'),
        description=_('Link to the class header on GitHub'),
        constraint = headerURL_constraint,
        required=True
    )

    # directives.widget(build=TextLinesFieldWidget)
    build = schema.Text(
        title = _(u"Compilation instructions"),
        description = _(u"Instructions how to build the component"),
        required = True,
    )

    mcnp = schema.Text(
        title = _(u"Instructions to generate MCNP(X) deck"),
        required = True
        )

    povray = schema.Text(
        title = _(u"Instructions to generate POV-Ray scene"),
        required = False
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
