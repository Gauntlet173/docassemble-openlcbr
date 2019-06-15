---
layout: docs
title: docassemble-openlcbr Demos
short_title: Demos
---
# Demos
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

If you receive an error running the Clio Integration demo, an API Key may need to be refreshed. Please contact the maintainer or
open an issue.
