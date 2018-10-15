# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.
## Requirements
* docassemble
## Installation Procedure
Use the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr
## Usage
Run the test interview in the playground.
## Current Issues:
* The database doesn't have plain-language descriptions of the legal issues and sub-issues.
* The images in the collapsing lists don't display as expected
* There may be a bug in openlcbr where it is not dropping all of the factors.
## Progress:
* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.
* Have got openlcbr running inside the package.
* Test database will now run if you create a DAStaticFile object from trade\_secret\_cases.yaml and pass it to run\_lcbr\_test()
* Test interview created, running, displaying output readably.
* Created prototype for improved explanation structure, and another for improved explanation display.
## Work Plan
* Have DocAssemble interview generate a case file to test against the database.
* Reformat openlcbr explanation output as structured data
* ... and much more.