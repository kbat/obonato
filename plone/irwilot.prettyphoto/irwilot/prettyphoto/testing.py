# -*- coding: utf-8 -*-
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_ID
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
from zope.configuration import xmlconfig

import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.collection')
except pkg_resources.DistributionNotFound:
    HAS_COLLECTION = False
else:
    HAS_COLLECTION = True


class PrettyPhotoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import irwilot.prettyphoto
        xmlconfig.file(
            'testing.zcml',
            irwilot.prettyphoto,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'irwilot.prettyphoto:testing')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("one_state_workflow")

        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Add a Folder
        portal.invokeFactory("Folder",
                             id="test-folder", title=u"Test Folder")

        # Add a Collection
        if HAS_COLLECTION:
            portal.invokeFactory('Collection',
                                 id="test-collection",
                                 title=u"Test Collection")

            query = [{
                'i': 'Type',
                'o': 'plone.app.querystring.operation.string.is',
                'v': 'Image',
            }]

            # set the query and publish the collection
            portal['test-collection'].setQuery(query)


IRWILOT_PRETTYPHOTO_FIXTURE = PrettyPhotoLayer()
IRWILOT_PRETTYPHOTO_INTEGRATION = IntegrationTesting(
    bases=(IRWILOT_PRETTYPHOTO_FIXTURE, ),
    name="irwilot.prettyphoto:Integration")
IRWILOT_PRETTYPHOTO_FUNCTIONAL = FunctionalTesting(
    bases=(IRWILOT_PRETTYPHOTO_FIXTURE, ),
    name="irwilot.prettyphoto:Functional")
IRWILOT_PRETTYPHOTO_ROBOT = FunctionalTesting(
    bases=(IRWILOT_PRETTYPHOTO_FIXTURE, z2.ZSERVER_FIXTURE),
    name="irwilot.prettyphoto:Robot")
