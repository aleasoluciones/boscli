# -*- coding: utf-8 -*-

import unittest
from doublex import *

import boscli
from boscli import exceptions, basic_types
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module


# cli# config
# cli (config)# interface eth 0/0
# cli (config-eth 0/0)# ip address 192.168.5.6
# cli (config-eth 0/0)# netmask 255.255.255.0
# cli (config-eth 0/0)# gateway 192.168.5.1
# cli (config-eth 0/0)# exit
# cli (config)#

# cli# config
# cli (config)#
# cli (config)# ip address 192.168.5.6
# cli (config)# ERROR unknown command



class InterpreterContextTest(unittest.TestCase):
    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.eth_configurator = Spy()
        self._add_command(['ip', 'address', basic_types.StringType()], self.eth_configurator.ip_address)
        self._add_command(['netmask', basic_types.StringType()], self.eth_configurator.netmask)
        self._add_command(['gateway', basic_types.StringType()], self.eth_configurator.gateway)
        self._add_command(['exit'], self.eth_configurator.commit)

    def _add_command(self, tokens, func):
        self.interpreter.add_command(boscli.Command(tokens, func))

    def test_normal_execution(self):
        self.interpreter.eval('ip address 192.168.5.6')
        self.interpreter.eval('netmask 255.255.255.0')
        self.interpreter.eval('gateway 192.168.5.1')
        self.interpreter.eval('exit')

        assert_that(self.eth_configurator.ip_address, called().with_args('192.168.5.6', ANY_ARG))
        assert_that(self.eth_configurator.netmask, called().with_args('255.255.255.0', ANY_ARG))
        assert_that(self.eth_configurator.gateway, called().with_args('192.168.5.1', ANY_ARG))
        assert_that(self.eth_configurator.commit, called().with_args(ANY_ARG))
