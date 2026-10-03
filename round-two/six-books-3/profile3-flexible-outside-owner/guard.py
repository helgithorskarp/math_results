"""Operational bounds only, never a mathematical exclusion."""
import time

LIMIT = 2000000
SECONDS = 40


class Limit(Exception):
    pass


class Guard:
    def __init__(self):
        self.started = time.monotonic()
        self.work = 0

    def tick(self):
        if self.work >= LIMIT or time.monotonic() - self.started >= SECONDS:
            raise Limit('Incomplete enumeration: no mathematical verdict')
        self.work += 1
