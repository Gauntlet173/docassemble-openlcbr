# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.
## Requirements
* docassemble
## Installation Procedure
Use the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr
## Usage
Install the package and run the explain\_lcbr\_test.yml interview to see the current state of development.
Load the db\_builder.yml interview for an interview that will assist you in building
your own analogical reasoning tools for use with docassemble-openlcbr.
## Demo
[Click here for a live demo of what the user sees](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fexplain_lcbr_test.yml)

[Click here for a live demo of how to build a reasoner](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fdb_builder.yml)
## Clio Integration Demo
As part of the sponsorship of the fellowship project, I have developed a version of the
explain\_lcbr\_test.yml interview which uses information obtained from a live
[Clio](http://www.clio.com) account, demonstrating the possibility of integrating
docassemble-openlcbr with live data acquired over the Clio API.

[Click here](https://testda.roundtablelaw.ca/interview?i=docassemble.openlcbr%3Adata%2Fquestions%2Fexplain_lcbr_test.yml)
for a live demo of the integration between Clio and docassemble-openlcbr.

The code for connecting to Clio is not included in docassemble-openlcbr, but may be
released later under a different package.

## Progress:
* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.
* Got openlcbr running inside the package.
* Test interview created, running, displaying output readably.
* Created prototype for improved explanation structure, and another for improved explanation display.
* Created DATree data structure for explanations with display\_tree() function for pretty-display
* Added plain-language description of issues to database.
* Modified openlcbr algorithm to generate explanation in DATree structure
* Implemented new version of ibp to utilize DATree structure for explanation.
* Changed explanation output to be natural language, narrative.
* Updated interview and lcbr to run the reasoner against a case specified by the user.
* Added an interview capable of building an openlcbr database from scratch.
* Added the ability to automatically generate a test-case query screen from the data source.
* Added the ability to edit a previously-generated openlcbr database.
## Work Plan
* New demonstration analogical reasoning database in a family law issue.
* Integrate the analogical reasoning tool with a wider-purpose demonstration interview.
* Create documentation and tutorials explaining how to use the system.