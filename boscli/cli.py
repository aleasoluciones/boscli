import boscli
from boscli import interpreter as interpreter_module

import readline


class CliInterface(object):

    def __init__(self, interpreter, readline_module=readline):
        self.interpreter = interpreter
        self.prompt = 'cli>'
        self.readline_module = readline_module

    def complete(self, prefix, index):
        line = self.readline_module.get_line_buffer()
        begin_idx = self.readline_module.get_begidx()
        end_idx = self.readline_module.get_endidx()
        print
        print "P", prefix
        print "L", line
        print "Indexes %d %d '%s'" % (begin_idx, end_idx, line[0:begin_idx])
        print "Completion '%s'" % (line[begin_idx:end_idx])
        return None

    def interact(self):
        while True:
            try:
                val = self.interpreter.eval(raw_input(self.prompt))
                if val is not None:
                    print str(val)
            except boscli.exceptions.NotMatchingCommandFoundError:
                print "Not matching command found"


def main():
    interpreter = interpreter_module.Interpreter()
    interpreter.add_command(boscli.Command(['net', 'show'], lambda *args, **kwargs: (args, kwargs)))
    interpreter.add_command(boscli.Command(['net', 'list'], lambda *args, **kwargs: (args, kwargs)))
    interpreter.add_command(boscli.Command(['net', 'add', 'host'], lambda *args, **kwargs: (args, kwargs)))
    cli = CliInterface(interpreter)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(cli.complete)
    cli.interact()

if __name__ == '__main__':
    main()
