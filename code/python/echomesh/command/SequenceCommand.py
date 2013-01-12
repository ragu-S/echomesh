from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command.CommandLoop import CommandLoop
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class SequenceCommand(CommandLoop):
  def __init__(self, score, element, timeout=None):
    CommandLoop.__init__(self, score, element, timeout, name='RandomCommand')
    self.commands = element.get('commands', [])
    self.next_command = 0

  def _command_time(self):
    return self.commands[self.next_command].get('time', 0) + self.start_time

  def _next_time(self, t):
    if self.next_command < len(self.commands):
      LOGGER.debug('Running command %d', self.next_command)
      return self._command_time()
    else:
      LOGGER.debug('Sequence finished')
      self.close()
      return 0

  def _command(self, t):
    while self.next_command < len(self.commands) and self._command_time() <= t:
      LOGGER.debug('%d', self.next_command)
      self.execute_command(self.commands[self.next_command])
      self.next_command += 1
