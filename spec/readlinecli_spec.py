from unittest.mock import patch, MagicMock

from boscli import exceptions
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

            with it('pauses the watchdog while the command runs and resumes it afterwards'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist', idle_timeout=300)

                with patch('boscli.readlinecli.readlinecli.IdleWatchdog') as MockWatchdog, \
                     patch('builtins.input', side_effect=['some_command', EOFError]):
                    mock_instance = MagicMock()
                    MockWatchdog.return_value = mock_instance
                    interpreter.eval.side_effect = lambda line: mock_instance.pause.assert_called_once()

                    cli.interact()

                    assert mock_instance.pause.call_count == 1
                    assert mock_instance.resume.call_count == 2

        with context('when a command raises'):
            with it('resumes the watchdog anyway'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.eval.side_effect = RuntimeError('boom')
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist', idle_timeout=300)

                with patch('boscli.readlinecli.readlinecli.IdleWatchdog') as MockWatchdog, \
                     patch('builtins.input', side_effect=['fail_cmd', EOFError]):
                    mock_instance = MagicMock()
                    MockWatchdog.return_value = mock_instance

                    cli.interact()

                    assert mock_instance.resume.call_count == 2

    with context('interact loop'):

        with context('when line ends with ?'):
            with it('prints help instead of evaluating the command'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.help.return_value = {'cmd': 'a help text'}
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('builtins.input', side_effect=['show?', EOFError]):
                    cli.interact()

                interpreter.help.assert_called_once_with('show')
                interpreter.eval.assert_not_called()

        with context('when a command evaluates to a value'):
            with it('prints the value and saves it to the audit file'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.eval.return_value = 'some_result'
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('builtins.input', side_effect=['some_command', EOFError]), \
                     patch.object(cli, '_save_command_with_timestamp') as mock_save, \
                     patch('builtins.print') as mock_print:
                    cli.interact()

                    interpreter.eval.assert_called_once_with('some_command')
                    mock_save.assert_called_once_with('some_command')
                    printed = [call.args[0] for call in mock_print.call_args_list if call.args]
                    assert 'some_result' in printed

        with context('when NoMatchingCommandFoundError is raised'):
            with it('prints no matching command and shows help'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.eval.side_effect = exceptions.NoMatchingCommandFoundError()
                interpreter.help.return_value = {}
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('builtins.input', side_effect=['bad_command', EOFError]):
                    cli.interact()

                interpreter.help.assert_called_once()

        with context('when AmbiguousCommandError is raised'):
            with it('prints the ambiguous command message with matching commands'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.eval.side_effect = exceptions.AmbiguousCommandError(['cmd1', 'cmd2'])
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('builtins.input', side_effect=['amb', EOFError]), \
                     patch('builtins.print') as mock_print:
                    cli.interact()

                    calls = [str(c) for c in mock_print.call_args_list]
                    assert any('Ambiguous command' in c for c in calls)

        with context('when a generic exception is raised'):
            with it('prints the exception details and keeps running'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                interpreter.eval.side_effect = [RuntimeError('boom'), None]
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist', debug=True)

                with patch('builtins.input', side_effect=['fail_cmd', 'ok_cmd', EOFError]), \
                     patch('builtins.print') as mock_print, \
                     patch('traceback.print_exc') as mock_traceback:
                    cli.interact()

                    mock_traceback.assert_called_once()
                    calls = [str(c) for c in mock_print.call_args_list]
                    assert any('Unknown exception' in c for c in calls)

    with context('completions_without_duplicates'):
        with it('merges completions with and without trailing space, removing duplicates'):
            interpreter = MagicMock()
            interpreter.prompt = 'test'
            interpreter.complete.return_value = ['show ', 'show', 'run ', 'exit ']
            cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

            result = cli.completions_without_duplicates('sh')

            assert 'show' in result
            assert 'run ' in result
            assert 'exit ' in result

    with context('complete'):
        with it('returns the index-th completion when available'):
            interpreter = MagicMock()
            interpreter.prompt = 'test'
            interpreter.complete.return_value = ['first', 'second ']
            cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

            with patch('readline.get_line_buffer', return_value='some_prefix'):
                first = cli.complete('some_prefix', 0)
                second = cli.complete('some_prefix', 1)
                missing = cli.complete('some_prefix', 5)

            assert first == 'first'
            assert second == 'second '
            assert missing is None

    with context('_save_command_with_timestamp'):
        with context('with an empty command'):
            with it('does not open the audit file'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                with patch('builtins.open') as mock_open:
                    cli._save_command_with_timestamp('')

                    mock_open.assert_not_called()

        with context('with a real command'):
            with it('appends the command with a timestamp to the audit file'):
                interpreter = MagicMock()
                interpreter.prompt = 'test'
                cli = readlinecli.ReadlineCli(interpreter, histfile='/tmp/.test_hist')

                mock_file = MagicMock()
                with patch('builtins.open', return_value=mock_file) as mock_open:
                    mock_file.__enter__.return_value = mock_file
                    cli._save_command_with_timestamp('show version')

                    mock_open.assert_called_once()
                    mock_file.write.assert_called_once()
                    written = mock_file.write.call_args[0][0]
                    assert 'show version' in written
