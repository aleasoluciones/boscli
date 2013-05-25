from boscli import exceptions

class Interpreter(object):
	def add_command(self, command):
		pass

	def eval(self, line_text):
		raise exceptions.NotMatchingCommandFound(line_text)