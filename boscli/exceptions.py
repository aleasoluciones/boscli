
class EvalError(Exception):
	pass

class NotMatchingCommandFoundError(EvalError):
	pass

class AmbiguousCommandError(EvalError):
	def __init__(self, *matching_commands):
		self.matching_commands = matching_commands
