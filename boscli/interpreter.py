from boscli import exceptions

class Interpreter(object):
	def __init__(self):
		self._commands = []

	def add_command(self, command):
		self._commands.append(command)

	def eval(self, line_text):
		matching_commands = []
		for command in self._commands:
			if command.match(line_text):
				matching_commands.append(command)
		if len(matching_commands) == 1:
			return matching_commands[0].execute(line=line_text, interpreter=self)
		elif len(matching_commands) > 0:
			raise exceptions.AmbiguousCommandError(matching_commands)

		if line_text:
			raise exceptions.NotMatchingCommandFoundError(line_text)