
class OptionsType(object):

	def __init__(self, valid_options):
		self.valid_options = valid_options

	def match(self, word, partial_line=None):
		return word in self.valid_options
