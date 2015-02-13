# -*- coding: utf-8 -*-

import os
import readline
import atexit
from boscli import exceptions



class ReadlineCli(object):

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.init_history()
        self.init_readline()

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


    def init_history(self):
        histfile=os.path.expanduser("~/.aleacli_history")
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
        

    def interact(self):
        while True:
            try:
                line = raw_input(self.interpreter.prompt + '>')
                if line.endswith('?'):
                    line = line[:-1]
                    commands_help = self.interpreter.help(line.strip())
                    for command_str in sorted(commands_help.keys()):
                        print str(command_str), ' ==> ', commands_help[command_str]
                else:
                    val = self.interpreter.eval(line)
                    if val is not None:
                        print str(val)
            except exceptions.NotMatchingCommandFoundError:
                print "Not matching command found"
            except exceptions.AmbiguousCommandError as exc:
                print "Ambigous command"
                for command in exc.matching_commands:
                    print "\t", command
            except (exceptions.EndOfProgram, EOFError, KeyboardInterrupt):
                print "Exit"
                break
