# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

long_description = open('README.md').read()


class MambaTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys
        import mamba.cli
        sys.argv = ['mamba']
        mamba.cli.main()

setup(name='boscli',
      version='0.9.2',
      author='Alea Soluciones SLL',
      author_email='eduardo.ferro.aldama@gmail.com',
      description ='Extensible command line processor for "ad hoc" shells creation',
      long_description=long_description,
      license='MIT',
      platforms = 'Linux',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'spec']),
      cmdclass={'test': MambaTest}
)
