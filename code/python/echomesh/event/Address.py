from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

# TODO: needs to be finished and integrated into the code.

"""

Format for an address!

tag:  [hello, world]       # A single tag or a list of tags.
platform:  [mac, pc, rp]
name: [chairman, president]

Either a string, which matches a name


"""
def match_one(them, us):
  return (not us) or


def match(from, to):
  from_ts = from.get('target'), from.get('source')
  to_ts = to.get('target'), to.get('source')

