# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import mamba.cli


class MambaTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys
        sys.argv = ['mamba']
        mamba.cli.main()

setup(name='boscli',
      version='0.0.1',
      author='Alea Soluciones SLL',
      description ='',
      platforms = 'Linux',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'spec']),
      cmdclass={'test': MambaTest}
)
