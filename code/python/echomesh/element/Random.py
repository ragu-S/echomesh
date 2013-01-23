from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Element
from echomesh.util.math import Poisson
from echomesh.element import Register

DEFAULT_INTERVAL = 10.0

class Random(Element.Element):
  def __init__(self, parent, description):
    super(Random, self).__init__(parent, description, name='RandomCommand')
    self.mean = description.get('mean', DEFAULT_INTERVAL)

    total_weight, weights_counted = 0, 0
    self.elements = []
    weights = []
    for choice in description.get('choices', []):
      weight = choice.get('weight', None)
      if weight is not None:
        assert weight >= 0, "Random weights can't be negative"
        weights_counted += 1
        total_weight += weight
      weights.append(weight)
      self.elements.(Load.make(self, choice['element']))

    if not weights_counted:
      total_weight, weights_counted = 1, 1

    mean_weight = total_weight / weights_counted
    total_weight = 0
    self.totals = []
    for i, w in enumerate(weights):
      total_weight += (mean_weight if w is None else w)
      self.totals.append(total_weight)

  def execute(self):
    rnd = random.random() * self.totals[-1]
    index = bisect.bisect_right(self.totals, rnd)
    element = self.elements(index)
    element.execute()


class RandomInterval(Element.Loop):
  def _next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def _command(self, t):
    self.execute_command(self.command)


def select_random(score, event, *choices):
  if choices:
    item = random.choice(choices)
    function_name = item.get('function', None)
    function = score.functions.get(function_name, None)
    if function:
      keywords = item.get('keywords', {})
      arguments = item.get('arguments', [])
      function(score, event, *arguments, **keywords)
    else:
      LOGGER.error('No function named "%s": %s, %s', function_name, item, choices)
  else:
    LOGGER.error('No arguments to select_random')

Register.register(Random)
