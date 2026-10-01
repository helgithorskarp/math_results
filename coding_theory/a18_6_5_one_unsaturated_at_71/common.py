"""Paths, exact serialization and non-escalating finite-case guards."""
from hashlib import sha256
from pathlib import Path
import os
import time

HERE = Path(__file__).resolve().parent
WORK = Path(os.environ.get("CWC_71_WORK", str(HERE / ".work")))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    import json
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


class Incomplete(Exception):
    pass


class Guard:
    def __init__(self, nodes=200000, seconds=10):
        require(type(nodes) is int and 0 <= nodes <= 200000, "invalid or escalated node guard")
        require(type(seconds) in (int, float) and 0 <= seconds <= 10, "invalid or escalated time guard")
        self.limit, self.seconds, self.nodes = nodes, seconds, 0
        self.started = time.monotonic()

    def tick(self):
        self.nodes += 1
        if self.nodes > self.limit or time.monotonic()-self.started > self.seconds:
            raise Incomplete("INCOMPLETE finite-case guard")


def bits(mask):
    while mask:
        first = mask & -mask
        yield first.bit_length()-1
        mask ^= first
