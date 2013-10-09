import boscli

from boscli import parser as parser_module
from boscli import interpreter as interpreter_module
from boscli import basic_types

import readline
import six


class ReadlineCli(object):

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.prompt = 'cli>'

    def complete(self, prefix, index):
        try:
            line = readline.get_line_buffer()
            completions = list(self.interpreter.complete(line))
            completions = completions + [None]
            return completions[index]
        except Exception as exc:
            print "Error", exc
            import traceback
            traceback.print_bt()

    def interact(self):
        while True:
            try:
                line = raw_input(self.prompt)
                if line.endswith('?'):
                    line = line[:-1]
                    for command, help in six.iteritems(self.interpreter.help(line)):
                        print str(command), ' ==> ', help
                else:
                    val = self.interpreter.eval(line)
                    if val is not None:
                        print str(val)
            except boscli.exceptions.NotMatchingCommandFoundError:
                print "Not matching command found"
            except Exception:
                import traceback
                traceback.print_exc()

class InterfaceConfigurator(object):
    def init_iface_conf(self, iface, interpreter, **kwargs):
        interpreter.push_context('iface_conf')
        print "init_iface_conf", iface, kwargs

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


def add_command(interpreter, keys, func, context_name=None):
    interpreter.add_command(boscli.Command(keys, func, context_name=context_name))

def main():
    parser = parser_module.Parser()
    interpreter = interpreter_module.Interpreter(parser)
    interface_configurator = InterfaceConfigurator()

    add_command(interpreter, ['iface', basic_types.OptionsType(['eth0', 'eth1', 'eth2'])], interface_configurator.init_iface_conf)
    add_command(interpreter, ['address', basic_types.StringType()], interface_configurator.address, context_name='iface_conf')
    add_command(interpreter, ['netmask', basic_types.StringType()], interface_configurator.netmask, context_name='iface_conf')
    add_command(interpreter, ['network', basic_types.StringType()], interface_configurator.network, context_name='iface_conf')
    add_command(interpreter, ['gateway', basic_types.StringType()], interface_configurator.gateway, context_name='iface_conf')
    add_command(interpreter, ['iface', 'commit'], interface_configurator.commit_iface_conf, context_name='iface_conf')

    cli = ReadlineCli(interpreter)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(cli.complete)
    cli.interact()

if __name__ == '__main__':
    main()
