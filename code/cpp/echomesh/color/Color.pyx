include "echomesh/color/FColor.pyx"
include "echomesh/color/ColorName.pyx"

import six

_COLOR_COMPARES = {
  0: lambda x: x < 0,
  1: lambda x: x <= 0,
  2: lambda x: x == 0,
  3: lambda x: x != 0,
  4: lambda x: x > 0,
  5: lambda x: x >= 0,
  }

cdef bool richcmpColors(FColor x, FColor y, int cmp):
  return _COLOR_COMPARES[cmp](x.compare(y))

def force_color(c):
  return c if isinstance(c, Color) else Color(c)

cdef class Color:
  cdef FColor* thisptr

  def __cinit__(self, *args):
    self.thisptr = new FColor()
    if len(args) == 1:
      args = args[0]
    if not fill_color(args, self.thisptr):
      raise ValueError('Can\'t construct color from "%s"' % str(args))

  @property
  def parts(self):
    p = self.thisptr.parts()
    return [p[0], p[1], p[2]]

  @property
  def alpha(self):
    return self.thisptr.alpha()
  # @property
  # def rgb(self):
  #   return [self.red, self.green, self.blue]

  # @property
  # def red(self):
  #   return self.thisptr.red()

  # @property
  # def green(self):
  #   return self.thisptr.green()

  # @property
  # def blue(self):
  #   return self.thisptr.blue()

  def scale(self, float f):
    scaleRgb(self.thisptr, f)

  def combine(self, Color c):
    combineRgb(c.thisptr[0], self.thisptr)

  def __dealloc__(self):
    del self.thisptr

  def __str__(self):
    return rgbToName(self.thisptr[0])

  def __repr__(self):
    return 'Color(%s)' % str(self)

  def __richcmp__(Color self, Color other, int cmp):
    return richcmpColors(self.thisptr[0], other.thisptr[0], cmp)

cdef bool fill_color(object x, FColor* c):
  if not x:
    c.copy(NO_COLOR)
    return True

  if isinstance(x, Color):
    c.copy((<Color> x).thisptr)
    return True

  elif isinstance(x, six.string_types):
    return nameToRgb(x, c)

  if isinstance(x, six.integer_types):
    c.copy(rgbFromInt(x))
    return True

  try:
    if len(x) == 3:
      c.copy(FColor(x[0], x[1], x[2], 1.0))
      return True

    if len(x) == 4:
      c.copy(FColor(x[0], x[1], x[2], x[3]))
      return True
  except:
    pass