from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from compatibility import six

from echomesh.base import Name
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml

def clean(*path):
  return os.path.join(*path).split('/')

def _command_file(*path):
  path = clean(*path)
  base = Path.ECHOMESH_PATH if path[0] == '4.default' else Path.PROJECT_PATH
  res = os.path.join(base, 'command', *path)
  return res

def _command_path():
  return ([
    '0.local',
    '1.name/' + Name.NAME] +
    [('2.tag/' + t) for t in Name.TAGS] +
    ['3.platform/' + Platform.PLATFORM,
     '4.global',
      _command_file('5.default')])

_COMMAND_PATH = _command_path()

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  path = clean(*path)
  return [os.path.join('command', i, *path) for i in _COMMAND_PATH]

def resolve(*path):
  x = expand(*path)
  for f in x:
    if os.path.exists(f):
      return f

def load(*path):
  data, error = None, None
  f = resolve(*path)
  if f:
    try:
      data = Yaml.read(f)
    except Exception as e:
      error = str(e)
    else:
      if not data:
        error = "Couldn't read Yaml from file %s" % os.path.join(*path)
  else:
    error = "Couldn't find file %s" % os.path.join(*path)

  return data, error

def config_file(scope):
  return _command_file(scope, 'config.yml')

def _recompute_command_path():
  def lookup(name):
    name_map, error = load(name)
    if name_map:
      return Name.lookup(Merge.merge(*name_map))

  name = lookup('name_map.yml')
  if name:
    Name.set_name(name)

  tags = lookup('tag_map.yml')
  if tags:
    if isinstance(tags, dict):
      print('Malformed tag_map.yml')
    else:
      if isinstance(tags, six.string_types):
        tags = [tags]
      Name.TAGS[:] = tags

_recompute_command_path()
_COMMAND_PATH = _command_path()
