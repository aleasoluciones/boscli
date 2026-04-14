import os
import time
import threading


class IdleWatchdog:

    def __init__(self, timeout_seconds):
        self._timeout = timeout_seconds
        self._last_activity = time.monotonic()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch, daemon=True)

    def start(self):
        self._thread.start()

    def touch(self):
        self._last_activity = time.monotonic()

    def stop(self):
        self._stop_event.set()

    def _watch(self):
        check_interval = min(60, self._timeout)
        while not self._stop_event.is_set():
            idle = time.monotonic() - self._last_activity
            if idle >= self._timeout:
                print(f"\nSession timed out after {self._timeout}s of inactivity. Exiting.", flush=True)
                os._exit(0)
            self._stop_event.wait(check_interval)
