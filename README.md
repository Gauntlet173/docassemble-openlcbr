# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.
## Requirements
* docassemble
## Installation Procedure
Use the docassemble package manager to add the package from https://github.com/Gauntlet173/docassemble-openlcbr
## Usage
Install the package and run the explain\_lcbr\_test.yml interview to see the current state of development.
## Current Issues:
* The images in the collapsing lists don't display as expected, this appears to be a
  caching problem on machines that have a prior version of the javascript.
## Progress:
* Matthias Grabmair backported openlcbr to Python 2.7 to make it easier to use with docassemble's module system.
* Have got openlcbr running inside the package.
* Test interview created, running, displaying output readably.
* Created prototype for improved explanation structure, and another for improved explanation display.
* Created DATree data structure for explanations with display\_tree() function for pretty-display
* Added plain-language description of issues to database.
* Modified openlcbr algorithm to generate explanation in DATree structure
* Implemented new version of ibp to utilize DATree structure for explanation.
* Changed explanation output to be natural language, narrative.
## Work Plan
* Allow the interview user to specify their own test case using docassemble variables.
* Automatically generate a test-case query interview
  based on an openlcbr factor database.
* Generate a new test reasoning database in a family law issue.
* Integrate the analogical reasoning tool with a wider-purpose demonstration interview.
* Create a docassemble interview that will allow a legal expert to create a new
  analogical reasoning database to be used in other interviews on the same server.
* Make the codebase less brittle.
* Create documentation explaining how to use the system.
* Have DocAssemble interview generate a case to test against the analogical reasoner.
* Integrate with Clio for selecting a test case.
* Integrate with Clio to use matters in a firm's database as a datasource for a
  predictive model.