---
layout: docs
title: Building Analogical Reasoners using docassemble-openlcbr
short_title: Building Analogical Reasoners
---
# Building Analogical Reasoners using docassemble-openlcbr

## Introduction

This document will guide you through the process of designing an analogical reasoner using openlcbr, using the the tools
provided by docassemble-openlcbr.

## Introduction to OpenLCBR

OpenLCBR is an open source project written by Matthias Grabmair on the basis of his academic work, and the work of Kevin Ashley and
OTHER PERSON.  OpenLCBR is re-implemented in docassemble-openlcbr, so the two projects may increasingly differ over time.

OpenLCBR is a tool for Legal Case-Based Reasoning (LCBR). At the time of writing, it implements a single algorithm, called Issue-Based
Prediction (IBP).  That is the algorithm implemented in docassemble-openlcbr.

For details on how the algorithm works, see ELSEWHERE.

This document provides advice on the task of building an analogical reasoner using docassemble-openlcbr, but is also applicable to any
project using OpenLCBR directly.

## Overview of the Development Process

### A Note on Expectations

Before we look at the process for developing analogical reasoner, let's be clear about what we are trying to accomplish. The objective
here is not to develop a tool that is capable of accurately predicting 100% of the fact scenarios presented to it.

The goal in using an analogical reasoning tool is to approximate the predictive power of a human expert or experts who design the tool.
In open-textured issues, even expert lawyers may be wrong a significant portion of the time. The law is uncertain.

So when evaluating the performance of your reasoner, or attempting to determine how to decide some issue described below, always keep
in mind the following question: "Does this matter in terms of generating predictions that are as reliable as the predictions I/we would
make with the same information?" If the answer is "no", then don't worry about it, and move on.

### 1 - Choose the legal issue

Although in theory the IBP algorithm can be used to decide any number of issues in a tree of issues, it is probably best to have
a single legal issue that the reasoner is intended to answer.  This legal issue should be what is called an "open-textured" issue.
An open-textured legal issue is one that cannot be determined solely by applying deductive logic to a known set of pieces of information.

For example, whether or not a person is a minor in a given jurisdiction depends on two things: what the age of majority is in that jurisdiction,
and the person's age.  Or, you can replace the person's age with the person's birth date and the current date. That is a legal issue that
can be answered by applying deductive logic to a known set of pieces of information, and is "closed-textured."

By way of comparison, whether or not a person has the capacity to draft a will is an "open-textured" question. Certainly, the person's
age will come into it, but there are also an unknown list of factors that might be important, or persuasive, or influence a decision-maker.

Not every open-textured legal issue will be a good choice for building an analgoical reasoner.  Here are some factors to consider.

1. Are there cases?
+
You can't build an analogical reasoner without cases for the reasoner to compare fact scenarios against. The best issues for automation
will have a database of cases that can be referred to.
2. Do the cases go in both directions?
+
An analogical reasoner based on IBP will not be able to make predictions unless there are cases in the database which have decided
the legal issue in different directions. If all of the times the matter has been decided it has been decided in the same way, that is not
a good candidate legal issue.
3. Are the cases detailed, and diverse?
+
The issue here is whether the cases provide the reasoner with enough information, and different enough information, in terms of the factors that led to the result.
In an OpenLCBR database, the same factors leading to the same result twice does not change the prediction compared to if they
happened only once.  The reasoner needs to have examples of different ways of coming to the same conclusions to be useful. Having cases
which are too similar to one another can happen if the number of factors is low (low detail), or if the factors are the same (low
diversity).
4. Is the area of law mature?
+
The question to consider at this point is whether it is likely that a large number of the relevant factors to this legal issue have
been discussed.  Court decisions will tend to limit their comments to those things which are disagreed-upon by the parties, and may
not even mention all of the factors that the parties and the court believed were relevant, but which were agreed-upon. So earlier
in the history of a legal issue, it is likely that not all of the relevant factors for that issue have ever been considered, or even
mentioned in cases.

You may not become aware of the factors that might make your legal issue inappropriate for automation until later in the
development process. These factors should be kept in mind throughout the process.

### Obtain a Database of Cases

Thte next step in designing an analogical reasoner is to decide on a database of cases to use.  There are a number of factors to
consider in the process of deciding which cases to include.

#### Issues Around Relative Persuasiveness
The IBP algorithm does not provide a mechanism for the legal knowledge engineer to indicate that some of the cases in the database
are of greater strength or importance than others.  The algorithm treats all cases as being of equal importance.  In the case of
cases which are dated, out of the ordinary, and not likely to be used as precedent in future decisions, it may be preferable to exclude
those cases from your database on that basis.

Where a case has been overturned by a higher court, and is not good law, that case should likely be excluded on that basis, if:
a) the higher court case will be in the database, and
b) the case was overturned on the legal issue you are trying to decide.

If, however, a case decided the issue you are trying to model, and was overturned on an unrelated issue, that case may be appropriate
to include in the database.

Where there are more important cases, such as cases decided by a higher court, you have to decide whether to include them in the
database, and how to deal with their difference in importance. It may be necessary to adjust your legal issues tree in order to account
for the importance of that case in particular circumstances. Perhaps an alternative way of finding the main issue should be provided.
The risk there is that the IBP algorithm does not distinguish between the cases which are relevant to the various issues in the tree.
For that reason, it may be better to divide the project into two different reasoners.  Or perhaps it is just a matter of their being
an overwhelmingly important factor in the first case, and that factor can be named as a knock-out factor.

#### Issues Around Availability

### 3. Determine Relevant Factors

### 4. Model the Legal Issue

#### List Knock-Out Factors

#### Decide the Issue Tree

##### Conjunctive and Subjunctive Sub-Issues


