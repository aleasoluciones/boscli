# -*- coding: utf-8 -*-


class EvalError(Exception):
    pass


class NoMatchingCommandFoundError(EvalError):
    pass


class AmbiguousCommandError(EvalError):
    def __init__(self, matching_commands):
        self.matching_commands = matching_commands
        super(AmbiguousCommandError, self).__init__(matching_commands)


class SintaxError(EvalError):
    pass


class NotContextDefinedError(Exception):
    pass


class EndOfProgram(Exception):
    pass
