from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.graphics import Shader
from echomesh.util import Log
from echomesh.util.thread import Runnable
from echomesh.util import ImportIf

pi3d = ImportIf.imp('pi3d')

LOGGER = Log.logger(__name__)

class Display(Runnable.Runnable):
  def __init__(self):
    super(Display, self).__init__()
    if not Config.get('load_module', 'pi3d'):
      self.display = None
      return

    keywords = {}

    background = Config.get('pi3d', 'background')
    if background:
      keywords.update(background=background)

    dimensions = Config.get('pi3d', 'dimensions')
    if dimensions:
      x, y, width, height = dimensions
      keywords.update(x=x, y=y, width=width, height=height)

    for k in ['aspect', 'depth', 'far', 'near', 'tk', 'window_title']:
      keywords[k] = Config.get('pi3d', k)

    self.display = pi3d.Display.create(**keywords)
    Config.add_client(self)
    Shader.SHADER()  # Make sure that the shader is created in the main thread!

  def config_update(self, get):
    if self.display:
      self.display.frames_per_second = get('pi3d', 'frames_per_second')

  def _on_run(self):
    super(Display, self)._on_run()
    if self.display:
      self.display.first_time = True
      self.display.is_running = True

  def _on_pause(self):
    super(Display, self)._on_pause()
    self.display and self.display.pause()

  def loop(self):
    while self.is_running and self.display and self.display.loop_running():
      pass

  # TODO: This is old code!
  def load_texture(self, imagefile):
    if imagefile == '$random':
      imagefile = random.choice(os.listdir(DEFAULT_IMAGE_DIRECTORY.directory))

    imagefile = DEFAULT_IMAGE_DIRECTORY.expand(imagefile)
    return self.texture_cache.create(imagefile)
