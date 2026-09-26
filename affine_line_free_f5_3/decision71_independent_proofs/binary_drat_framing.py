#!/usr/bin/env python3
"""Check binary DRAT framing and hash bytes; never check proof validity.

The accepted subformat has a/d command bytes, canonical unsigned base-128
literal codes in [2, 2**31-1], and a zero byte ending each clause.  The low
bit encodes sign.  Empty streams and semantically false proofs can pass.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path


class BinaryDratFraming:
    """Incremental syntax guard, suitable for an existing hashing loop."""

    def __init__(self):
        self.digest = sha256()
        self.bytes = self.additions = self.deletions = self.literals = 0
        self.empty_clauses = self.max_variable = self.clause_literals = 0
        self.prefix = True
        self.shift = self.value = 0

    def fail(self, reason):
        raise ValueError(f"byte {self.bytes - 1}: {reason}")

    def feed(self, block):
        self.digest.update(block)
        for byte in block:
            self.bytes += 1
            if self.prefix:
                if byte not in (97, 100):
                    self.fail("expected binary addition/deletion prefix")
                self.additions += byte == 97
                self.deletions += byte == 100
                self.prefix = False
                self.clause_literals = 0
                continue
            if byte == 0:
                if self.shift:
                    self.fail("noncanonical or truncated literal encoding")
                self.empty_clauses += self.clause_literals == 0
                self.prefix = True
                continue
            self.value |= (byte & 127) << self.shift
            if self.value > 2**31 - 1:
                self.fail("literal code exceeds the pinned C decoder's signed int")
            if byte & 128:
                self.shift += 7
                if self.shift > 28:
                    self.fail("literal encoding is too long")
                continue
            if self.value < 2:
                self.fail("signed zero is not a literal")
            self.max_variable = max(self.max_variable, self.value >> 1)
            self.literals += 1
            self.clause_literals += 1
            self.shift = self.value = 0

    def finish(self):
        if not self.prefix:
            raise ValueError("EOF before a complete clause terminator")
        return {
            "status": "BINARY_DRAT_FRAMING_VALID",
            "syntax_only": True,
            "global_unsat_accepted": False,
            "bytes": self.bytes,
            "sha256": self.digest.hexdigest(),
            "additions": self.additions,
            "deletions": self.deletions,
            "literals": self.literals,
            "empty_clauses": self.empty_clauses,
            "max_variable": self.max_variable,
        }


def inspect(path, chunk_size=1 << 20):
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    check = BinaryDratFraming()
    with Path(path).open("rb") as stream:
        while block := stream.read(chunk_size):
            check.feed(block)
    return check.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.proof), indent=2, sort_keys=True))
