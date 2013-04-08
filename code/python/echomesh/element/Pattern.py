from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import LightSingleton
from echomesh.element import Element

class Pattern(Element.Element):
  def __init__(self, parent, description):
    super(Pattern, self).__init__(parent, description)
    assert parent.__class__.__name__ == 'Light'
    self.pattern_name = description['pattern']
    self.renderer = parent.renderers[self.pattern_name]
    self.output = description.get('output', 'light')
    if self.output == 'light':
      LightSingleton.add_owner()

  def _on_unload(self):
    if self.output == 'light':
      LightSingleton.remove_owner()
      LightSingleton.remove_client(self.renderer)

  def class_name(self):
    return 'pattern(%s)' % self.pattern_name

  def _on_run(self):
    super(Pattern, self)._on_run()
    if self.output == 'light':
      LightSingleton.add_client(self.renderer)

  def _on_pause(self):
    super(Pattern, self)._on_pause()
