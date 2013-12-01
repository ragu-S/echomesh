from __future__ import absolute_import, division, print_function, unicode_literals

import os

from distutils.core import Command
from echomesh.base import Platform
from echomesh.build.BuildConfig import CONFIG

COMMANDS = {
  'darwin': ('xcodebuild -project Builds/MacOSX/echomesh.xcodeproj '
             '-configuration {Config}')
}

class Library(Command):
  description = 'Build C++ library'
  user_options = []
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    command = COMMANDS.get(Platform.PLATFORM)
    if command:
      config = 'debug' if CONFIG.debug else 'release'
      command = command.format(config=config, Config=config.capitalize())
      print('Building library with command\n', '  ', command)
      if os.system(command):
        raise Exception('Library command failed')

