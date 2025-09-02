import sys
import re

class ByLineBaseFilter:
    def __init__(self):
        self.output = ''

    def write(self, data):
        self.output += data
        k = self.output.rfind('\n')
        if k != -1:
            data_to_flush = self.output[:k]
            for line in data_to_flush.splitlines():
                self.process_line(line)
            self.output = self.output[k+1:]

    def flush(self):
        # only works by line, so ignore any flush
        pass

    def process_line(self, line):
        pass

class IncludeFilter(ByLineBaseFilter):
    def __init__(self, regex, stdout):
        self.regex = re.compile(regex)
        self.stdout = stdout
        super().__init__()

    def process_line(self, line):
        if self.regex.search(line):
            self.stdout.write(line + '\n')


class ExcludeFilter(ByLineBaseFilter):
    def __init__(self, regex, stdout):
        self.regex = re.compile(regex)
        self.stdout = stdout
        super().__init__()

    def process_line(self, line):
        if not self.regex.search(line):
            self.stdout.write(line + '\n')


class RedirectStdout:
    ''' Create a context manager for redirecting sys.stdout
        to another file.
    '''
    def __init__(self, new_target):
        self.new_target = new_target
        self.old_target = None

    def __enter__(self):
        self.old_target = sys.stdout
        sys.stdout = self.new_target
        return self

    def __exit__(self, exctype, excinst, exctb):
        sys.stdout = self.old_target


class FilterFactory:
    def create_include_filter(self, reg_ex, output):
        return IncludeFilter(reg_ex, output)

    def create_exclude_filter(self, reg_ex, output):
        return ExcludeFilter(reg_ex, output)
