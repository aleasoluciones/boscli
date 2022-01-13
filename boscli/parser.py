import shlex


class Parser:

    def parse(self, input_line):
        tokens = shlex.split(input_line)
        if input_line.endswith(' '):
            tokens.append('')
        return tokens
