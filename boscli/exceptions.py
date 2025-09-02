class EvalError(Exception):
    pass


class NoMatchingCommandFoundError(EvalError):
    pass


class AmbiguousCommandError(EvalError):
    def __init__(self, matching_commands):
        self.matching_commands = matching_commands
        super().__init__(matching_commands)


class SyntaxError(EvalError):
    pass


class NotContextDefinedError(Exception):
    pass


class EndOfProgram(Exception):
    pass
