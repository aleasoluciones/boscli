from boscli import exceptions

class Interpreter(object):
	def __init__(self):
		self._commands = []

	def add_command(self, command):
		self._commands.append(command)

	def eval(self, line_text):
		if not line_text:
			return
		
		matching_commands = self._select_matching_commands(line_text)
		
		if len(matching_commands) == 1:
			return matching_commands[0].execute(line=line_text, interpreter=self)
		if len(matching_commands) > 0:
			raise exceptions.AmbiguousCommandError(matching_commands)
		raise exceptions.NotMatchingCommandFoundError(line_text)

	def _select_matching_commands(self, line_text):
		return [command for command in self._commands if command.match(line_text)]

