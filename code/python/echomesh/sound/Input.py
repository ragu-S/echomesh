from __future__ import absolute_import, division, print_function, unicode_literals

import analyse
import numpy

class Input(object):
  def __init__(self):
    self.frames = self.numpy_frames = self.level = None

  def receive(self, frames):
    self.frames = frames
    self.numpy_frames = numpy.fromstring(frames, dtype=self.dtype, count=-1)
    self.level = analyse.loudness(self.numpy_frames)
