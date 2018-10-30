#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.openlcbr',
      version='0.3.1',
      description=('A docassemble extension implementing legal case-based reasoning based via openlcbr by Matthias Grabmair.'),
      long_description="# docassemble-openlcbr\r\nA docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.\r\n## Requirements\r\n* docassemble\r\n## Installation Procedure\r\nUse the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr\r\n## Usage\r\nInstall the package and run the explain\\_lcbr\\_test.yml interview to see the current state of development.\r\nLoad the db\\_builder.yml interview for an interview that will assist you in building\r\nyour own analogical reasoning tools for use with docassemble-openlcbr.\r\n## Demo\r\n[Click here for a live demo of what the user sees](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fexplain_lcbr_test.yml)\r\n[Click here for a live demo of how to build a reasoner](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdb_builder.yml)\r\n## Current Issues:\r\n* The images in the collapsing lists don't display as expected, this appears to be a\r\n  caching problem on machines that have a prior version of the javascript.\r\n## Progress:\r\n* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.\r\n* Got openlcbr running inside the package.\r\n* Test interview created, running, displaying output readably.\r\n* Created prototype for improved explanation structure, and another for improved explanation display.\r\n* Created DATree data structure for explanations with display\\_tree() function for pretty-display\r\n* Added plain-language description of issues to database.\r\n* Modified openlcbr algorithm to generate explanation in DATree structure\r\n* Implemented new version of ibp to utilize DATree structure for explanation.\r\n* Changed explanation output to be natural language, narrative.\r\n* Updated interview and lcbr to run the reasoner against a case specified by the user.\r\n* Added an interview capable of building an openlcbr database from scratch.\r\n## Work Plan\r\n* Automatically generate a test-case query interview based on an openlcbr factor database.\r\n* Generate a new demonstration analogical reasoning database in a family law issue.\r\n* Integrate the analogical reasoning tool with a wider-purpose demonstration interview.\r\n* Allow convenient editing of existing openlcbr analogical reasoning databases on the server.\r\n* Make the codebase less brittle.\r\n* Create documentation and tutorials explaining how to use the system.\r\n* Integrate with Clio for selecting a test case.\r\n* Integrate with Clio to use matters in a firm's database as a datasource for a\r\n  predictive model.",
      long_description_content_type='text/markdown',
      author='Jason Morris',
      author_email='jason@roundtablelaw.ca',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/openlcbr/', package='docassemble.openlcbr'),
     )

