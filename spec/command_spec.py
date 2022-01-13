from hamcrest import is_
from doublex import assert_that

from boscli.command import Command

with describe('Command'):
    with it('Allow to assign a command ID'):
        command = Command(['k1', 'k2'], cmd_id='cmd_id1')

        assert_that(command.cmd_id, is_('cmd_id1'))
