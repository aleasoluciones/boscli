from unittest.mock import patch, MagicMock

from boscli import interpreter as interpreter_module
from boscli.readlinecli import readlinecli


with describe('ReadlineCli'):

    with context('idle timeout'):

        with context('when idle_timeout is provided'):
            with it('creates and starts a watchdog during interact'):
                interpreter = interpreter_module.Interpreter(prompt='test')
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist', idle_timeout=300)

                with patch('boscli.readlinecli.readlinecli.IdleWatchdog') as MockWatchdog, \
                     patch('builtins.input', side_effect=EOFError):
                    mock_instance = MagicMock()
                    MockWatchdog.return_value = mock_instance

                    cli.interact()

                    MockWatchdog.assert_called_once_with(300)
                    mock_instance.start.assert_called_once()
                    mock_instance.stop.assert_called_once()

        with context('when idle_timeout is not provided'):
            with it('does not create a watchdog'):
                interpreter = interpreter_module.Interpreter(prompt='test')
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('boscli.readlinecli.readlinecli.IdleWatchdog') as MockWatchdog, \
                     patch('builtins.input', side_effect=EOFError):

                    cli.interact()

                    MockWatchdog.assert_not_called()

        with context('when a command is executed'):
            with it('touches the watchdog after each input'):
                interpreter = interpreter_module.Interpreter(prompt='test')
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist', idle_timeout=300)

                with patch('boscli.readlinecli.readlinecli.IdleWatchdog') as MockWatchdog, \
                     patch('builtins.input', side_effect=['some_command', 'another_command', EOFError]):
                    mock_instance = MagicMock()
                    MockWatchdog.return_value = mock_instance

                    cli.interact()

                    assert mock_instance.touch.call_count == 2
