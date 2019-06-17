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
      version='0.5.4',
      description=('A docassemble extension implementing legal case-based reasoning based via openlcbr by Matthias Grabmair.'),
      long_description=u'# docassemble-openlcbr\r\nA docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.\r\n\r\n[This post](https://medium.com/@jason_90344/legal-expert-systems-just-got-smarter-e7e12b75e872) is a primer\r\non what an analogical reasoner does, and why it\'s important to have one in the open-source toolkit.\r\n\r\n[This post](https://medium.com/@jason_90344/automating-case-based-reasoning-by-analogy-a-deep-dive-a1b015f234dd) provides\r\na full explanation of how the IBP algorith, which docassemble-openlcbr implements, works.\r\n\r\n## Requirements\r\n* [docassemble](https://docassemble.org/)\r\n## Installation Procedure\r\nUse the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr\r\n## Usage\r\nLoad the db\\_builder.yml interview for an interview that will assist you in building\r\nyour own analogical reasoning tools for use with docassemble-openlcbr. That interview\r\nwill provide you with a leave-one-out accuracy rating when the interview is complete.\r\n\r\nIn order to debug your reasoner, use the deep\\_reasoner\\_test.yml interview to view the\r\ndetailed results of all leave-one-out tests of the prediction algorithm.\r\n\r\nOnce you have a working reasoner, implement it in your docassemble interview by\r\nfollowing these steps:\r\n\r\n1. Upload your reasoner file into the sources directory in docassemble.\r\n2. Include `.ibp_data` in the `modules` block of your interview.\r\n3. Include the following lines in the `objects` block of your interview, replacing\r\n   `reasoner_name.yml` with the name of the file you uploaded:\r\n```\r\nobjects:\r\n  - reasoner: DAIBPData\r\n  - database: DAStaticFile.using(filename="data/sources/reasoner_name.yml")\r\n  - test_case: DAIBPCase\r\n```\r\n4. In your interview, populate the DAList `test_case.factors` with the factor IDs from your\r\n   reasoner that are relevant to your test case.\r\n5. Call `reasoner.load(database)` to initialize the reasoner. If you do not want to\r\n   include the cases listed in your database, you can call `reasoner.load_model_only(database)`,\r\n   and then cases can be added to the reasoner using `reasoner.add_precedent_case(case)`\r\n   where `case` is a DAIBPCase object with attributes of `.id`, `.winner` (either \'p\'\r\n   or \'d\'), and `.factors` as in a test case.\r\n6. Call `reasons = reasoner.predict(test_case, issue="id of root issue")`, replacing\r\n   "id of root issue" with the id you gave to the root issue in your database. It will\r\n   return a DATree object which is the explanation of the result.\r\n7. Obtain the result of the prediction by looking at `reasons.prediction`. The value \'p\'\r\n   indicates that the outcome was predicted for the plaintiff, \'d\' for the defendant,\r\n   and \'a\' indicates that the reasoner abstained. To display a user-friendly version\r\n   call `prediction_word(reasons.prediction)`, but be aware that what the reasoner\r\n   considers \'plaintiff\' may represent \'true\' in your interview, so `prediction_word`\r\n   is not always appropriate.\r\n8. To display the reasons to the user, you must include the following in the\r\n   `features` block of your interview:\r\n```\r\nfeatures:\r\n  javascript: docassemble.openlcbr:data/static/list_collapse.js\r\n  css: docassemble.openlcbr:data/static/list_collapse.css\r\n```\r\n9. Then, use `reasons.display_tree()` to display a collapsing tree interface of\r\n   the reasoner\'s results.\r\n\r\n## Demos\r\nThere are four live demos of docassemble-openlcbr functionality available. The source code for all the demos is included\r\nin the package:\r\n\r\n0. The [Trade Secrets demo](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fexplain_lcbr_test.yml)\r\n   is a minimal implementation of docassemble-openlcbr.\r\n1. The [AIP Tool](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Faip_tool.yml)\r\n   demonstrates a real-world use of an analogical reasoner built using\r\n   docassemble-openlcbr, and display\'s the reasoner\'s reasons on the last page of\r\n   the interview.\r\n2. The [Reasoner Builder](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdb_builder.yml)\r\n   can be used to create a reasoner database and get a raw\r\n   leave-one-out predictive score.\r\n3. The [Deep Reasoner Tester](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdeep_reasoner_tester.yml) can be used to see the reasons of all the leave-one-out\r\n   tests in order to troubleshoot bad predictions.\r\n\r\n## Clio Integration Demo\r\nThanks to Clio\'s sponsorship of the ABA Fellowship Project, there is also a version of the\r\nTrade Secret interview which uses information obtained from a live\r\n[Clio](http://www.clio.com) account, demonstrating the possibility of integrating\r\ndocassemble-openlcbr with live data acquired over the Clio API.\r\n\r\nIn this demo, both the information from the test case and the precedents are obtained\r\nfrom the live Clio account.  Only the factors and the issue model need to be specified\r\nin the database.\r\n\r\n[Click here](https://testda.roundtablelaw.ca/interview?i=docassemble.clio%3Adata%2Fquestions%2Fclio_openlcbr_demo.yml)\r\nfor a live demo of the integration between Clio and docassemble-openlcbr.\r\n\r\n## Documentation\r\nA number of blog posts about the project are available at \r\n[Jason Morris\' Medium page](https://medium.com/@jason_90344).\r\n\r\nDocumentation for docassemble-openlcbr is still a work in progress, and will be available at\r\n[https://gauntlet173.github.io/docassemble-openlcbr/](https://gauntlet173.github.io/docassemble-openlcbr/).\r\n\r\n## Help\r\nPlease report issues at the docassemble-openlcbr [GitHub](https://github.com/Gauntlet173/docassemble-openlcbr).\r\n\r\nFor support, join the #analogyproject channel at the [docassemble slack](https://docassemble.slack.com).\r\n\r\nTo offer feedback, contact [Jason Morris](https://www.twitter.com/RoundTableLaw).\r\n\r\n## Thanks\r\n* Kevin Ashley and Stefanie Bruninghaus for developing the IBP Algorithm\r\n* Matthias Grabmair for the Python implementation of IBP in [openlcbr]() on which\r\n  docassemble-openlcbr is based. (And for re-implementing it in Python 2.7!)\r\n* The American Bar Association Center for Innovation, and in particular\r\n  Chase Hertel, Sarah Glassmeyer, and Joshua Furlong, who were particularly involved\r\n  in selecting my proposal.\r\n* Jack Newton, Joshua Lenon, and Chris Thompson of Clio, who were instrumental in\r\n  my fellowship receiving sponsorship funding from Clio.\r\n* Jonathan Pyle, for developing docassemble, and for his constant and expert\r\n  assistance over the three months that this project was underway.\r\n* The docassemble user community who were extremely helpful and patient with a lawyer\r\n  who was learning docassemble and Python.\r\n  \r\n## Version History\r\n0.5.0 - First "feature complete" version.\r\n0.5.3 - Fixed - Periods of Separation Not Working\r\n0.5.4 - Fixed - Problems adding and editing factors',
      long_description_content_type='text/markdown',
      author='Jason Morris',
      author_email='jason@roundtablelaw.ca',
      license='The MIT License (MIT)',
      url='https://Gauntlet173.github.io/docassemble-openlcbr',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/openlcbr/', package='docassemble.openlcbr'),
     )

