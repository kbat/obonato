from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='kbat.content',
      version=version,
      description="kbat content package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['kbat'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
#         'Plone',
          'plone.app.dexterity [grok]',
#          'collective.autopermission',
          'plone.app.referenceablebehavior',
          'plone.namedfile [blobs]',
#          'cioppino.twothumbs',
#        'zopeskel.dexterity',
#        'paste.script.templates',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
