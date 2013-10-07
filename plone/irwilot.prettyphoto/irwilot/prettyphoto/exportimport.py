from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPropertiesTool

# Properties are defined here, because if they are defined in
# propertiestool.xml, all properties are re-set the their initial state if you
# reinstall product in the quickinstaller.

_PROPERTIES = [
    dict(name='speed', type_='string', value='normal'),
    dict(name='opacity', type_='string', value='0.80'),
    dict(name='show_title', type_='boolean', value=True),
    dict(name='show_description', type_='boolean', value=True),
    dict(name='counter_sep', type_='string', value='/'),
    dict(name='theme', type_='string', value='dark_rounded'),
    dict(name='autoplay', type_='boolean', value=True),
    dict(name='autoplay_slideshow', type_='boolean', value=False),
    dict(name='iframe_width', type_='string', value='75%'),
    dict(name='iframe_height', type_='string', value='75%'),
    dict(name='overlay_gallery', type_='boolean', value=False),
    dict(name='slideshow', type_='int', value=0),
    dict(name='deeplinking', type_='boolean', value=False),
    dict(name='social_tools', type_='string', value=''), # social_tools example:   <div class="pp_social"><div class="twitter"><a href="http://twitter.com/share" class="twitter-share-button" data-count="none">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script></div><div class="facebook"><iframe src="http://www.facebook.com/plugins/like.php?locale=en_US&href='+location.href+'&amp;layout=button_count&amp;show_faces=true&amp;width=500&amp;action=like&amp;font&amp;colorscheme=light&amp;height=23" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:500px; height:23px;" allowTransparency="true"></iframe></div></div>
]

def configureKupu(kupu):

    paragraph_styles = list(kupu.getParagraphStyles())

    new_styles = [
        ('prettyPhoto', 'prettyPhoto Link|a'),
        ('prettyPhotoIframe', 'prettyPhoto Iframe Link|a'),
    ]
    to_add = dict(new_styles)

    for style in paragraph_styles:
        css_class = style.split('|')[-1]
        if css_class in to_add:
            del to_add[css_class]

    if to_add:
        paragraph_styles += ['%s|%s' % (v, k) for k, v in new_styles if \
                             k in to_add]
        kupu.configure_kupu(parastyles=paragraph_styles)


def import_various(context):
    if not context.readDataFile('irwilot.prettyphoto.txt'):
        return

    site = context.getSite()

    # skip kupu configuration on sites that don't have kupu installed
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        configureKupu(kupu)

    # Define portal properties
    ptool = getToolByName(site, 'portal_properties')
    props = ptool.prettyphoto_properties

    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'],
                                     prop['type_'])
