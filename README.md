# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.

[This post](https://medium.com/@jason_90344/legal-expert-systems-just-got-smarter-e7e12b75e872) is a primer
on what an analogical reasoner does, and why it's important to have one in the open-source toolkit.

[This post](https://medium.com/@jason_90344/automating-case-based-reasoning-by-analogy-a-deep-dive-a1b015f234dd) provides
a full explanation of how the IBP algorith, which docassemble-openlcbr implements, works.

## Requirements
* [docassemble](https://docassemble.org/)
## Installation Procedure
Use the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr
## Usage
Load the db\_builder.yml interview for an interview that will assist you in building
your own analogical reasoning tools for use with docassemble-openlcbr. That interview
will provide you with a leave-one-out accuracy rating when the interview is complete.

In order to debug your reasoner, use the deep\_reasoner\_test.yml interview to view the
detailed results of all leave-one-out tests of the prediction algorithm.

Once you have a working reasoner, implement it in your docassemble interview by
following these steps:

1. Upload your reasoner file into the sources directory in docassemble.
2. Include `.ibp_data` in the `modules` block of your interview.
3. Include the following lines in the `objects` block of your interview, replacing
   `reasoner_name.yml` with the name of the file you uploaded:
```
objects:
  - reasoner: DAIBPData
  - database: DAStaticFile.using(filename="data/sources/reasoner_name.yml")
  - test_case: DAIBPCase
```
4. In your interview, populate the DAList `test_case.factors` with the factor IDs from your
   reasoner that are relevant to your test case.
5. Call `reasoner.load(database)` to initialize the reasoner. If you do not want to
   include the cases listed in your database, you can call `reasoner.load_model_only(database)`,
   and then cases can be added to the reasoner using `reasoner.add_precedent_case(case)`
   where `case` is a DAIBPCase object with attributes of `.id`, `.winner` (either 'p'
   or 'd'), and `.factors` as in a test case.
6. Call `reasons = reasoner.predict(test_case, issue="id of root issue")`, replacing
   "id of root issue" with the id you gave to the root issue in your database. It will
   return a DATree object which is the explanation of the result.
7. Obtain the result of the prediction by looking at `reasons.prediction`. The value 'p'
   indicates that the outcome was predicted for the plaintiff, 'd' for the defendant,
   and 'a' indicates that the reasoner abstained. To display a user-friendly version
   call `prediction_word(reasons.prediction)`, but be aware that what the reasoner
   considers 'plaintiff' may represent 'true' in your interview, so `prediction_word`
   is not always appropriate.
8. To display the reasons to the user, you must include the following in the
   `features` block of your interview:
```
features:
  javascript: docassemble.openlcbr:data/static/list_collapse.js
  css: docassemble.openlcbr:data/static/list_collapse.css
```
9. Then, use `reasons.display_tree()` to display a collapsing tree interface of
   the reasoner's results.

## Demos
There are four live demos of docassemble-openlcbr functionality available. The source code for all the demos is included
in the package:

0. The [Trade Secrets demo](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fexplain_lcbr_test.yml)
   is a minimal implementation of docassemble-openlcbr.
1. The [AIP Tool](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Faip_tool.yml)
   demonstrates a real-world use of an analogical reasoner built using
   docassemble-openlcbr, and display's the reasoner's reasons on the last page of
   the interview.
2. The [Reasoner Builder](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdb_builder.yml)
   can be used to create a reasoner database and get a raw
   leave-one-out predictive score.
3. The [Deep Reasoner Tester](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdeep_reasoner_tester.yml) can be used to see the reasons of all the leave-one-out
   tests in order to troubleshoot bad predictions.

## Clio Integration Demo
Thanks to Clio's sponsorship of the ABA Fellowship Project, there is also a version of the
Trade Secret interview which uses information obtained from a live
[Clio](http://www.clio.com) account, demonstrating the possibility of integrating
docassemble-openlcbr with live data acquired over the Clio API.

In this demo, both the information from the test case and the precedents are obtained
from the live Clio account.  Only the factors and the issue model need to be specified
in the database.

[Click here](https://testda.roundtablelaw.ca/interview?i=docassemble.clio%3Adata%2Fquestions%2Fclio_openlcbr_demo.yml)
for a live demo of the integration between Clio and docassemble-openlcbr.

## Documentation
A number of blog posts about the project are available at 
[Jason Morris' Medium page](https://medium.com/@jason_90344).

Documentation for docassemble-openlcbr is still a work in progress, and will be available at
[https://gauntlet173.github.io/docassemble-openlcbr/](https://gauntlet173.github.io/docassemble-openlcbr/).

## Help
Please report issues at the docassemble-openlcbr [GitHub](https://github.com/Gauntlet173/docassemble-openlcbr).

For support, join the #analogyproject channel at the [docassemble slack](https://docassemble.slack.com).

To offer feedback, contact [Jason Morris](https://www.twitter.com/RoundTableLaw).

## Thanks
* Kevin Ashley and Stefanie Bruninghaus for developing the IBP Algorithm
* Matthias Grabmair for the Python implementation of IBP in [openlcbr]() on which
  docassemble-openlcbr is based. (And for re-implementing it in Python 2.7!)
* The American Bar Association Center for Innovation, and in particular
  Chase Hertel, Sarah Glassmeyer, and Joshua Furlong, who were particularly involved
  in selecting my proposal.
* Jack Newton, Joshua Lenon, and Chris Thompson of Clio, who were instrumental in
  my fellowship receiving sponsorship funding from Clio.
* Jonathan Pyle, for developing docassemble, and for his constant and expert
  assistance over the three months that this project was underway.
* The docassemble user community who were extremely helpful and patient with a lawyer
  who was learning docassemble and Python.
  
## Version History

* 0.5.0 - First "feature complete" version.
* 0.5.3 - Fixed - Periods of Separation Not Working
* 0.5.4 - Fixed - Problems adding and editing factors