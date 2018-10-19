from docassemble.base.core import DAObject, DAList
from docassemble.base.util import *

href_counter = 0

class DATree(DAObject):
  def init(self, *pargs, **kwargs):
    self.initializeAttribute('branches',DAList)
    self.branches.object_type = DATree
    self.branches.there_is_another = False
    return super(DATree, self).init(*pargs, **kwargs)
  def summary(self):
    # Return the Root Object
    return self.name + "\n\n" + self.href + "\n\n" + self.branches
  def display_tree(self, root_node=True):
    global href_counter
    href_counter = href_counter+1
    self.href = "item" + str(href_counter)
    has_branches = len(self.branches.elements) > 0
    output = ""
    if root_node:
      output += "<div class=\"just-padding\">"
    if root_node and has_branches:
      output += "<div class=\"list-group list-group-root\">"
    if has_branches:
      output += "<a href=\"#" + self.href + "\" class=\"list-group-item list-group-item-action\" data-toggle=\"collapse\">"
      output += "<i class=\"fa fa-caret-right\"></i>"
    else:
      output += "<div class=\"list-group-item list-group-item-action\">"
    output += self.text
    if has_branches:
      output += "</a>"
    else:
      output += "</div>"
    if has_branches:
      output += "<div class=\"list-group collapse\" id=\"" + self.href + "\">"
      for b in self.branches:
        output += b.display_tree(False)
      output += "</div>"
    if root_node and has_branches:
      output += "</div>"
    if root_node:
      output += "</div>"
    return output