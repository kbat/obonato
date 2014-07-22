from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from lizardie.content import MessageFactory as _

from lizardie.content.TradeItem import TradeItem as  Item
import pickle
from BeautifulSoup import BeautifulSoup

# Interface class; used to define content-type schema.

class ITender(form.Schema, IImageScaleTraversable):
    """
    Summary tender table
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/tender.xml to define the content type.

    form.model("models/tender.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Tender(Container):
    grok.implements(ITender)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# tender_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(ITender)
    grok.require('zope2.View')
    
    def table(self):
        with open("/home/kbat/prog/tender/data.pickle") as fb:
            items = pickle.load(fb)

        out = """
<table align='center' class='listing'>
<thead>
 <tr>
  <th>&#8470;</th><th>Auction</th><th>Lot &#8470;</th><th>Lot</th><th>Start price</th><th>Organizer</th><th>Application end date</th><th>Auction date</th><th>State</th><th>Winner</th>
 </tr>
</thead>
<tbody>
"""
        for i in items:
            out += '<tr>'
            out += '<td>' + i.n + '</td>'
            out += '<td>' + i.auction + '</td>'
            out += '<td>' + i.nlot + '</td>'
            out += '<td>' + i.lot + '</td>'
            out += '<td>' + i.startPrice + '</td>'
            out += '<td>' + i.organizer + '</td>'
            out += '<td>' + i.applicationEndDate + '</td>'
            out += '<td>' + i.date + '</td>'
            out += '<td>' + i.state + '</td>'
            if i.winner:
                out += '<td>' + i.winner + '</td>'
            else:
                out += '<td></td>'
            out += '</tr>'

        out += "</tbody></table>"
        return out

    # grok.name('view')

    # Add view methods here
