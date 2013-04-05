from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.Expression import Expression
from echomesh.expression.Units import INFINITY
from echomesh.graphics import Shader
from echomesh.util import Log
from echomesh.util.file import DefaultFile
from echomesh.util.thread.Runnable import Runnable
from echomesh.util import ImportIf

pi3d = ImportIf.imp('pi3d')

LOGGER = Log.logger(__name__)

DEFAULT_Z = 100.0

IMAGE_DIRECTORY = DefaultFile.DefaultFile('asset/image')

class ImageSprite(Runnable):
  CACHE = None

  def __init__(self, element, loops=1,
               position=(0, 0), rotation=(0, 0, 0),
               size=1, duration=None, z=DEFAULT_Z,
               shader=None, **kwds):
    super(ImageSprite, self).__init__()
    self.element = element
    self.imagename = IMAGE_DIRECTORY.expand(kwds.pop('file', None))
    del kwds['type']
    if kwds:
      s = '' if len(kwds) == 1 else 's'
      LOGGER.error('Unknown keyword%s: %s', s, ', '.join(kwds))

    self._loops = loops
    self._loop_number = 0
    self._position = Expression(position, element)
    self._rotation = Expression(rotation, element)
    self._size = Expression(size, element)
    self._z = Expression(z, element)
    self.element.time = 0   # elapsed time.
    self._time = 0  # start time.
    if duration is None:
      for env in [self._position, self._rotation, self._size, self._z]:
        if env.is_constant():
          duration = max(duration, env.length)
      if duration is None:
        duration = Units.INFINITY
    else:
      self._duration = Units.convert(duration)

    if not self._duration:
      LOGGER.warning('An image sprite had a zero duration.')
    if not ImageSprite.CACHE:
      ImageSprite.CACHE = pi3d.TextureCache()

    texture = ImageSprite.CACHE.create(self.imagename)
    x, y, z = self.coords()
    self.sprite = pi3d.ImageSprite(texture,
                                   w=texture.ix, h=texture.iy,
                                   shader=Shader.shader(shader),
                                   x=x, y=y, z=z)
    self.sprite.repaint = self.repaint

  def coords(self):
    x, y = self._position()
    z = self._z()
    return x, y, z

  def repaint(self, t):
    if not self._time:
      self._time = t
    elapsed = t - self._time
    if elapsed > self._duration:
      self._loop_number += 1
      if self._loop_number < self._loops:
        self._time = 0
        elapsed = 0
      else:
        LOGGER.debug('Finishing image sprite')
        self.pause()
        return

    self.element.time = elapsed
    self.sprite.position(*self.coords())
    size = self._size()
    self.sprite.scale(size, size, size)
    xrot, yrot, zrot = self._rotation()
    self.sprite.rotateToX(xrot)
    self.sprite.rotateToY(yrot)
    self.sprite.rotateToZ(zrot)
    self.sprite.draw()

  def _on_run(self):
    super(ImageSprite, self)._on_run()
    self._add_sprite()

  def _add_sprite(self):
    pi3d.Display.Display.INSTANCE.add_sprites(self.sprite)

  def _on_pause(self):
    super(ImageSprite, self)._on_pause()
    pi3d.Display.Display.INSTANCE.remove_sprites(self.sprite)


