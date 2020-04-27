# -*- coding: utf-8 -*-
from cl.content.content.component import IComponent  # NOQA E501
from cl.content.testing import CL_CONTENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ComponentIntegrationTest(unittest.TestCase):

    layer = CL_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_component_schema(self):
        fti = queryUtility(IDexterityFTI, name='Component')
        schema = fti.lookupSchema()
        self.assertEqual(IComponent, schema)

    def test_ct_component_fti(self):
        fti = queryUtility(IDexterityFTI, name='Component')
        self.assertTrue(fti)

    def test_ct_component_factory(self):
        fti = queryUtility(IDexterityFTI, name='Component')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IComponent.providedBy(obj),
            u'IComponent not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_component_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Component',
            id='component',
        )

        self.assertTrue(
            IComponent.providedBy(obj),
            u'IComponent not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('component', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('component', parent.objectIds())

    def test_ct_component_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Component')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
