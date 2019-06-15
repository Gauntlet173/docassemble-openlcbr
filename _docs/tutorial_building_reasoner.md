---
layout: docs
title: Building Case-Based Reasoners with docassemble-openlcbr
short_title: Building Reasoners
---
# Building Reasoners

The process for building a reasoner using docassemble-openlcbr is simple. You just run the db\_builder.yml interview provided
in the package.  That interview will ask you to specify factors, cases, issues, and knock-out factors for your analogical
reasoner.

Remember that due to the limitations of Docassemble, you cannot use the "Back" button to go back to an earlier part of the
interview. If you don't want to lose your changes, finish the interview, download the reasoner file that it generates,
then restart the interview and upload the saved file.

This tutorial is a quick introduction to how to generate a reasoner database.  For detailed information see the main docs.

## What is a Factor?
A factor is something that is either true or false about a case, and which makes it more likely that the legal issue
will be determined for one party or the other.

## What is a case?
A case is a single occasion on which a court has decided the legal issue, and requires you to record the factors that were
true in that case, and the outcome of that case.

## What is an issue?
IBP allows you to specify the legal issues as a tree of issues and sub-issues. Each one has a name, and a default outcome.
Each also has a list of factors that are relevant for that issue.

## What are Knock-Out Factors?
A knock-out factor is a factor that is so important to decisions in this legal issue that cases that have that factor can be
ignored when trying to predict cases that don't.

## How Building a Reasoner Works

The workflow for building a reasoner works like this:

1. Find your cases, and enter them in the [DB Builder] to create a new database.
2. Read the cases, and for each one:

    a. If there are new factors present in that case, add them to the database. (Also review whether these factors were present in
     cases you have already covered).
     
    b. Record in the cases section of the [DB Builder] the factors that exist in that case.
    
    c. Note if there are different issues in that case, and add them to the database.
    
    d. Note what factors were relevant to what issues in that case, and edit the issues accordingly if necessary.
    
3. Download the database and upload it into the [deep DB tester] interview. Review the results to see what cases are predicted,
   and which are not. Make changes to your
   factors, issues, and knock-out factors to tune the performance of the database.
4. Download the tuned database, and upload it to the sources section of your Docassemble server.
5. Monitor the law for additional relevant cases, and update your database as required.

