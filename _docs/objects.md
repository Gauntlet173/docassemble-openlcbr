---
layout: docs
title: docassemble-oepnlcbr Objects
short_title: Objects
---
# docassembl-openlcbr Objects

## DAIBPData

## DAIBPIssue

## DAIBPCase

## DATree

DATree is a simple docassemble object that has a single attribute, `branches` which is a DAList of DATree objects. To use it,
simply create a root DATree object, and then append additional DATree objects to the `branches` list. Each of the branch objects
is also a DATree object by default, so each branch can have its own branches, on and on recursively.

You can then use `generic object:` blocks to build a tree, but it requires a little but of manipulating docassemble's workflow.

```
objects:
  - root: DATree
---
Put example here.
```

### Displaying a DATree

docassemble-openlcbr includes the ability to display a DATree in the interview as a set of collapsing fields.

To do this, you must include the javascript and css files included in docassemble-openlcbr as follows:

```
show features
```

Then, at the point in the interview where you want to display the tree, use the `display_tree()` function of the DATree object,
as follows:

```
show code
```
