# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.
## Requirements
* docassemble
## Installation Procedure
Use the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr
## Current Issues:
* Newlines in the ibp output are not being displayed correctly in docassemble.
## Progress:
* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.
* Have got openlcbr running inside the package.
* Test database will now run if you create a DAStaticFile object and pass it to run\_lcbr\_test()
* Test interview created
## Work Plan
* Have DocAssemble interview generate a case file to test against the database.
* Reformat openlcbr explanation output as structured data
* and much more.