from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='lizardie.content',
      version=version,
      description="lizardie content package",
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
      namespace_packages=['lizardie'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
#         'Plone',
          'plone.app.dexterity [grok]',
#          'collective.autopermission',
          'plone.app.referenceablebehavior',
          'plone.app.relationfield',
          'plone.namedfile[blobs]',
          'plone.formwidget.namedfile',
          'collective.dexteritytextindexer',
          'BeautifulSoup', # for pickle in tender.py
#          'cioppino.twothumbs',
          'sc.social.like',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
