from boscli import exceptions

class Interpreter(object):
	def __init__(self):
		self._commands = []

	def add_command(self, command):
		self._commands.append(command)

	def eval(self, line_text):
		for command in self._commands:
			if command.match(line_text):
				return command.execute(line=line_text, interpreter=self)

		if line_text:
			raise exceptions.NotMatchingCommandFound(line_text)