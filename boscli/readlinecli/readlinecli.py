import os
import time
import traceback
import readline
import atexit
from boscli import exceptions

try:
    input = raw_input
except NameError:
    pass


class ReadlineCli:

    def __init__(self, interpreter, debug=False, histfile="~/.history"):
        self.interpreter = interpreter
        self.init_history(histfile)
        self.init_readline()
        self.debug = debug
        self.completions = None
        self.histfile = histfile

    def init_readline(self):
        self._default_parse_and_bind()
        readline.parse_and_bind("set bell-style none")
        readline.parse_and_bind("set show-all-if-ambiguous")
        readline.parse_and_bind("set completion-query-items -1")
        readline.set_completer_delims(' \t\n')
        readline.set_completer(self.complete)

    def _default_parse_and_bind(self):
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")

    def init_history(self, histfile):
        histfile = os.path.expanduser(histfile)
        histfile = os.path.expandvars(histfile)
        try:
            readline.read_history_file(histfile)
        except IOError:
            pass
        atexit.register(self._save_history, histfile)

    def _save_history(self, histfile):
        readline.write_history_file(histfile)

    def completions_without_duplicates(self, line):
        completions = self.interpreter.complete(line)
        completions_with_spaces = [completion for completion in completions if completion.endswith(' ')]
        completions_without_spaces = [completion for completion in completions if not completion.endswith(' ')]

        results = completions_without_spaces
        for completion in completions_with_spaces:
            if completion.strip() not in results:
                results.append(completion)
        return results

    def complete(self, prefix, index):
        line = readline.get_line_buffer()

        response = None
        if index == 0:
            # This is the first time for this text, so build a match list.
            self.completions = self.completions_without_duplicates(line)

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.completions[index]
        except IndexError:
            response = None
        return response

    def _print_help(self, line):
        help_lines = []
        commands_help = self.interpreter.help(line.strip())
        for command_str in sorted(commands_help.keys()):
            help_lines.append(str(command_str) + ' ==> ' + (commands_help[command_str] or 'No help'))

        for help_line in sorted(help_lines):
            print(help_line)

    def _save_command_with_timestamp(self, command):
        if not command:
            return
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = os.path.expanduser(self.histfile + ".audit")
        with open(filename, "a") as file:
            file.write("{} - {}\n".format(timestamp, command))

    def interact(self):
        while True:
            try:
                line = input(self.interpreter.prompt + ' > ')
                if line.endswith('?'):
                    line = line[:-1]
                    self._print_help(line)
                else:
                    val = self.interpreter.eval(line)
                    self._save_command_with_timestamp(line)
                    if val is not None:
                        print(str(val))
            except exceptions.NoMatchingCommandFoundError:
                print("No matching command found")
                self._print_help(line)
            except exceptions.AmbiguousCommandError as exc:
                print("Ambiguous command")
                for command in exc.matching_commands:
                    print("\t", command)
            except (exceptions.EndOfProgram, EOFError, KeyboardInterrupt):
                print("Exit")
                break
            except Exception as exc:
                print("Unknown exception", exc, exc.__class__.__name__)
                if self.debug:
                    traceback.print_exc()
