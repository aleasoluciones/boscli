# -*- coding: utf-8 -*-

import boscli

from boscli import interpreter as interpreter_module
from boscli import basic_types
from boscli.command import Command
from boscli.readlinecli import readlinecli
import readline
import six



class InterfaceConfigurator(object):

    def init_iface_conf(self, iface, interpreter, **kwargs):
        interpreter.push_context('iface_conf', prompt='conf %s' % iface)
        print "init_iface_conf"

    def address(self, address, interpreter, **kwargs):
        interpreter.actual_context().data['address'] = address

    def netmask(self, netmask, interpreter, **kwargs):
        interpreter.actual_context().data['netmask'] = netmask

    def network(self, network, interpreter, **kwargs):
        interpreter.actual_context().data['network'] = network

    def gateway(self, gateway, interpreter, **kwargs):
        interpreter.actual_context().data['gateway'] = gateway

    def commit_iface_conf(self, interpreter, **kwargs):
        print "commit_iface_conf", kwargs
        print "Commit data"
        print interpreter.actual_context().data
        interpreter.pop_context()


def add_command(interpreter, keys, func, context_name=None, allways=False):
    interpreter.add_command(Command(keys, func, context_name=context_name, allways=allways))


def main():
    interpreter = interpreter_module.Interpreter(prompt='ifaces')
    interface_configurator = InterfaceConfigurator()

    add_command(
        interpreter, ['exit'], lambda *args, **kwargs: interpreter.exit(), allways=True)
    add_command(interpreter, ['iface', basic_types.OptionsType(
        ['eth0', 'eth1', 'eth2'])], interface_configurator.init_iface_conf)
    add_command(
        interpreter, ['address', basic_types.StringType(name='ip_address')],
        interface_configurator.address, context_name='iface_conf')
    add_command(
        interpreter, ['netmask', basic_types.StringType(name='netmask')],
        interface_configurator.netmask, context_name='iface_conf')
    add_command(
        interpreter, ['network', basic_types.StringType(name='network')],
        interface_configurator.network, context_name='iface_conf')
    add_command(
        interpreter, ['gateway', basic_types.StringType(name='ip_address')],
        interface_configurator.gateway, context_name='iface_conf')
    add_command(interpreter, ['iface', 'commit'],
                interface_configurator.commit_iface_conf, context_name='iface_conf')

    cli = readlinecli.ReadlineCli(interpreter)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(cli.complete)
    cli.interact()

if __name__ == '__main__':
    main()
