class Command(object):
	def __init__(self, *args):
		raise NotImplementedError()

	def match(self, *args):
		raise NotImplementedError()

	def execute(self, interpreter=None, line=None):
		raise NotImplementedError