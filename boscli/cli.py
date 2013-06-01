import boscli
from boscli import interpreter as interpreter_module

class CliInterface(object):
	def __init__(self, interpreter):
		self.interpreter = interpreter
		self.prompt = 'cli>'

	def interact(self	):
		while True:
			val = self.interpreter.eval(raw_input(self.prompt))
			if val is not None: 
				print str(val)

def main():
	interpreter = interpreter_module.Interpreter()
	interpreter.add_command(boscli.Command(['net', 'show'], lambda *args, **kwargs: (args, kwargs)))
	interpreter.add_command(boscli.Command(['net', 'list'], lambda *args, **kwargs: (args, kwargs)))
	interpreter.add_command(boscli.Command(['net', 'add', 'host'], lambda *args, **kwargs: (args, kwargs)))
	cli = CliInterface(interpreter)
	cli.interact()

if __name__ == '__main__':
	main()