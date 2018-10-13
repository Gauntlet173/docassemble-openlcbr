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
      version='0.1.1',
      description=('A docassemble extension implementing legal case-based reasoning based via openlcbr by Matthias Grabmair.'),
      long_description="# docassemble-openlcbr\r\nA docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.\r\n## Requirements\r\n* docassemble\r\n## Installation Procedure\r\nUse the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr\r\n## Usage\r\nRun the test interview in the playground.\r\n## Current Issues:\r\n* The database doesn't have plain-language descriptions of the legal issues and sub-issues.\r\n## Progress:\r\n* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.\r\n* Have got openlcbr running inside the package.\r\n* Test database will now run if you create a DAStaticFile object from trade\\_secret\\_cases.yaml and pass it to run\\_lcbr\\_test()\r\n* Test interview created, running, displaying output readably.\r\n## Work Plan\r\n* Have DocAssemble interview generate a case file to test against the database.\r\n* Reformat openlcbr explanation output as structured data\r\n* ... and much more.",
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

