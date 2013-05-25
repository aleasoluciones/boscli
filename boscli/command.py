class Command(object):
	def __init__(self, keywords, command_function = None):
		self.keywords = keywords
		self.command_function = command_function
		
	def match(self, line):
		return line.split() == self.keywords

	def execute(self, interpreter=None, line=None):
		if self.command_function:
			return self.command_function(line=line, interpreter=interpreter)

		