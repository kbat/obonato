from setuptools import setup, find_packages
import os

version = '2.0'

setup(name='ess.fastneutronsworkshop',
      version=version,
      description="ESS fast neutrons workshop management",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='conference management plone zope',
      author='Based on collective.conference developed by Inigo Consulting',
      author_email='',
      url='',
      license='GPLv2+',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ess'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.namedfile [blobs]',
          'collective.miscbehaviors>=0.2.1',
          'plone.formwidget.captcha',
          'incf.countryutils',
          'collective.js.fullcalendar',
          'collective.js.jqueryui',
          'z3c.table',
          'plone.z3ctable',
          'Products.AdvancedQuery',
          'collective.z3cform.colorpicker'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
