---
layout: docs
title: docassemble-openlcbr Overview
short_title: Overview
---
# Overview of docassemble-openlcbr

## What is d-o for?

Docassemble-openlcbr is an extension to docassemble that allows you to use legal case-based reasoning in your docassemble projects.

Legal case-based reasoning is a technology that allows a computer to make predictions about the outcome of an open-textured
legal issue and to explain its reasons for that prediction.

An open-textured legal issue is a subjective legal issue.  For example, a closed-textured question might be "are you old enough to vote?" 
That question can be answered definitively if you know the individual's birthdate, or their age, and you know the minimum age required to vote.
By contrast, an example of an open-textured question might be "did you use reasonable force?" There is no formula that can be used to come up with the right answer, every time.
Instead, a legal professional will compare the current fact scenario to fact scenarios that have been decided by the courts in the past,
and make a prediction about the likely outcome in the current fact scenario.

Legal case-based reasoning mimics that process, having the computer do the comparisons and the prediction.

Docassemble-openlcbr implements an algorithm called Issue-Based Prediction, which is explained in more detail elswhere in the documentation.

If you want to use docassemble to automate a legal service, but automating that legal service requires obtaining a prediction
as to one or more open-textured legal issues, docassemble-openlcbr can be used to automate those predictions.

## How do you use it?

Docassemble-openlcbr is installed on your docassemble server as a docassemble package.  Then, you can use the utilities it provides to build
and test an analogical reasoner.  This requires describing the issue and its sub-issues, setting out the relevant factors and how they
relate to the issues and sub-issues, and then entering a database of previously-decided cases.

Building the reasoner happens inside an easy-to-use docassemble interview. Once the reasoner is built, the package includes a testing utility to allow you to determine whether your reasoner is working as expected.  Once you are satisfied with the strength of your reasoner, you install it on your docassemble server.

In the docassemble interview, you create a test case object, and you have the user answer questions about all the factors relevant to the open-textured issue.  Those factors are added to the test case object, and the test-case object is sent to your reasoner.

The interview can then get a prediction from the reasoner, and can display the reasoner's explanation for that prediction, if desired.

## How well does it work?

An analogical reasoner is limited by the legal issue, the available data, and the skill and expertise of the person building the reasoner. In academic research, IBP reasoners have reached accuracies of approximately 92% in leave-one-out testing, with databases of more than 150 cases.  The demonstration database included with the docassemble-openlcbr database has only 28 cases, and abstains on predicting 4 of those cases. Of the other 24, it predicts 22 correctly, for an accuracy of almost 92%.  The demonstration database was generated using the tools provided in the docassemble-openlcbr package, and including time for legal research took approximately 25 hours to generate and test.
