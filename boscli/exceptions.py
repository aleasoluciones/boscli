
class EvalError(Exception):
	pass

class NotMatchingCommandFound(EvalError):
	pass

class AmbiguousCommandError(EvalError):
	def __init__(self, *matching_commands):
		self.matching_commands = matching_commands
