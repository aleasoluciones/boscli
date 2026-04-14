import time
from unittest.mock import patch

from hamcrest import assert_that, is_
from doublex import Spy, called, never

from boscli.idle_watchdog import IdleWatchdog


with describe('IdleWatchdog'):

    with context('when idle time exceeds timeout'):
        with it('calls os._exit'):
            with patch('boscli.idle_watchdog.os._exit') as mock_exit:
                watchdog = IdleWatchdog(timeout_seconds=1)
                watchdog.start()
                time.sleep(2)
                watchdog.stop()

                assert_that(mock_exit.call_count, is_(1))
                assert_that(mock_exit.call_args[0][0], is_(0))

    with context('when activity resets the timer'):
        with it('does not exit while touch is called'):
            with patch('boscli.idle_watchdog.os._exit') as mock_exit:
                watchdog = IdleWatchdog(timeout_seconds=2)
                watchdog.start()

                for _ in range(3):
                    time.sleep(1)
                    watchdog.touch()

                watchdog.stop()

                assert_that(mock_exit.call_count, is_(0))

    with context('when stopped before timeout'):
        with it('does not call os._exit'):
            with patch('boscli.idle_watchdog.os._exit') as mock_exit:
                watchdog = IdleWatchdog(timeout_seconds=2)
                watchdog.start()
                time.sleep(0.5)
                watchdog.stop()
                time.sleep(2)

                assert_that(mock_exit.call_count, is_(0))
