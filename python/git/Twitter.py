from __future__ import absolute_import, division, print_function, unicode_literals

import twitter

from util import Platform
from util import String

TWITTER_SIZE = 140

def get_api(auth, name=''):
  return twitter.Api(**auth['twitter'][name or Platform.NODENAME])

def post_update(text, auth, *names):
  text = String.truncate(text, TWITTER_SIZE)
  for name in names:
    get_api(auth, name).PostUpdate(text)
  return text
