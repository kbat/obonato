from logging import getLogger
from plone.browserlayer import utils as layerutils
from irwilot.prettyphoto.interfaces import IPrettyPhotoSpecific

log = getLogger('irwilot.prettyphoto')


def resetLayers(context):
    """Remove custom browserlayer on uninstall."""

    if context.readDataFile('irwilot.prettyphoto_uninstall.txt') is None:
        return

    if IPrettyPhotoSpecific in layerutils.registered_layers():
        layerutils.unregister_layer(name='irwilot.prettyphoto')
        log.info('Browser layer "irwilot.prettyphoto" uninstalled.')
