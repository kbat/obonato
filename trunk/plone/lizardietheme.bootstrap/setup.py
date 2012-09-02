from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='lizardietheme.bootstrap',
      version=version,
      description="Plone theme based on Twitter's Bootstrap CSS",
      long_description=open("README.rst").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='plone diazo theme',
      author='Izhar Firdaus',
      url='https://github.com/kagesenshi/lizardietheme.bootstrap',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['lizardietheme'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.theming',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
