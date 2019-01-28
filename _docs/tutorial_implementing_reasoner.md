---
layout: docs
title: docassemble-openlcbr Implementing Reasoner Tutorial
short_title: Implementing Reasoner Tutorial
---
# Implementing Reasoners in your Docassemble Interviews

Once you have generated a reasoner and installed it on your docassemble server, using the reasoner in your interview requires only a few steps.

## Include the IBP_Data Module

You need to include the ibp_data module in order to get access to the object definitions for [DAIBPData] and [DAIBPCase].

{% highlight yaml %}
---
modules:
  - .ibp_data
---
{% endhighlight %}

## Include the Formatting For Output

The package comes with javascript and css files which are used to provide a cascading tree interface for explanations.
If you wish to display explanations, you need to include the following in your features block:

{% highlight yaml %}
---
features:
  javascript: docassemble.openlcbr:data/static/list_collapse.js
  css: docassemble.openlcbr:data/static/list_collapse.css
{% endhighlight %}

## Generate the Required Objects

Once the module is loaded, in the objects block of your reasoner, you must create the following three objects.

{% highlight yaml %}
objects:
  - reasoner: DAIBPData
  - database: DAStaticFile.using(filename="data/sources/your_reasoner.yml")
  - test_case: DAIBPCase
{% endhighlight %}

[DAIBPData] is the reasoner object itself.  [DAIBPCase] is the test case format. You would replace "your_reasoner.yml" with the name
you gave to your own reasoner file.

## Populate the Test Case with Factors

Then, in your interview, you need to add factors to the test_case.factors DAList. Any method can be used
to add factors to this list, but the objects added to the list must have a name that is equal to the factor's ID
in your reasoner.  For example, the following code adds a factor with an ID of "F1".

{% highlight yaml %}
test_case.factors.append("F1")
{% endhighlight %}

## Initiate the Reasoner

In a mandatory code block, initiate the reasoner by loading the database file.

{% highlight yaml %}
---
mandatory: True
code: |
  reasoner.load(database)
---
{% endhighlight %}

## Get a Prediction

Once you are done adding factors to your test case, and the reasoner is initialized, you can obtain the prediction and reasons
as follows:

{% highlight yaml %}
reasons = reasoner.predict(test_case, issue="relationship of interdependence")
{% endhighlight %}

The "reasons" variable created above with have a `reasons.prediction` value which will be either 'p', 'd', or 'a' for Plaintiff,
Defendant, or Abstain.

## Display Reasons

Displaying the reasoner's explanation for the prediction in the interview is as simple as making a call to `reasons.display_tree()`.

{% highlight yaml %}
  ${reasons.display_tree()}
{% endhighlight %}
