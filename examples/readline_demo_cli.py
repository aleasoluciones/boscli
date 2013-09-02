import boscli

from boscli import parser as parser_module
from boscli import interpreter as interpreter_module
from boscli import completer as completer_module

import readline


class ReadlineCli(object):

    def __init__(self, interpreter, completer):
        self.interpreter = interpreter
        self.completer = completer
        self.prompt = 'cli>'

    def complete(self, prefix, index):
        try:
            line = readline.get_line_buffer()
            begin_idx = readline.get_begidx()
            end_idx = readline.get_endidx()
            completions = list(self.completer.complete(line))
            completions = completions + [None]
            return completions[index]
        except Exception as exc:
            print "Error", exc
            import traceback
            traceback.print_bt()

    def interact(self):
        while True:
            try:
                line = raw_input(self.prompt)
                if line.endswith('?'):
                    line = line[:-1]
                    for command, help in self.interpreter.help(line).iteritems():
                        print str(command), ' ==> ', help
                else:
                    val = self.interpreter.eval(line)
                    if val is not None:
                        print str(val)
            except boscli.exceptions.NotMatchingCommandFoundError:
                print "Not matching command found"
            except Exception as exc:
                import traceback
                traceback.print_exc()


def main():
    parser = parser_module.Parser()
    interpreter = interpreter_module.Interpreter(parser)
    completer = completer_module.Completer(interpreter, parser)
    interpreter.add_command(boscli.Command(['net', 'show'], lambda *args, **kwargs: (args, kwargs), help="net show help"))
    interpreter.add_command(boscli.Command(['net', 'list'], lambda *args, **kwargs: (args, kwargs), help="net list help"))
    interpreter.add_command(boscli.Command(['net', 'add', 'host'], lambda *args, **kwargs: (args, kwargs)))
    cli = ReadlineCli(interpreter, completer)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(cli.complete)
    cli.interact()

if __name__ == '__main__':
    main()
