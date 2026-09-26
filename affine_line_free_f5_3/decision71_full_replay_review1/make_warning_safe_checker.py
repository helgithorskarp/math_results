#!/usr/bin/env python3
"""Make the two-call diagnostic-only DRAT-trim sanitizer source patch."""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path


STOCK_SOURCE_SHA256 = "d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee"
WARNING_SAFE_SOURCE_SHA256 = (
    "12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0"
)

PRINTER = b'''static inline void printClause (int* clause) {
  printf ("[%i] ", clause[ID]);
  while (*clause) printf ("%i ", *clause++); printf ("0\\n"); }
'''

SAFE_PRINTER = PRINTER + b'''
/* A parser buffer has no negative clause-metadata slots.  Keep warnings and
   their control flow, but do not read clause[ID] when printing raw input. */
static inline void printRawClause (int* clause) {
  printf ("[raw] ");
  while (*clause) printf ("%i ", *clause++); printf ("0\\n"); }
'''

UNSAFE_UNIT = (
    b'printf ("\\rc WARNING: backward mode ignores deletion of (pseudo) unit '
    b'clause ");\n          printClause (buffer); }'
)
SAFE_UNIT = (
    b'printf ("\\rc WARNING: backward mode ignores deletion of (pseudo) unit '
    b'clause ");\n          printRawClause (buffer); }'
)
UNSAFE_MISSING = (
    b'printf ("\\rc WARNING: deleted clause on proof line %i does not occur: ", '
    b"fileLine); printClause (buffer); }"
)
SAFE_MISSING = (
    b'printf ("\\rc WARNING: deleted clause on proof line %i does not occur: ", '
    b"fileLine); printRawClause (buffer); }"
)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def patch_source(source: bytes) -> bytes:
    if digest(source) != STOCK_SOURCE_SHA256:
        raise ValueError("input is not the pinned stock DRAT-trim source")
    for needle, count in (
        (PRINTER, 1),
        (UNSAFE_UNIT, 1),
        (UNSAFE_MISSING, 1),
    ):
        if source.count(needle) != count:
            raise ValueError("pinned diagnostic patch context is not unique")
    result = source.replace(PRINTER, SAFE_PRINTER)
    result = result.replace(UNSAFE_UNIT, SAFE_UNIT)
    result = result.replace(UNSAFE_MISSING, SAFE_MISSING)
    if result.count(b"printClause (buffer)") != 0:
        raise ValueError("an unsafe raw-buffer printer remains")
    if result.count(b"printRawClause (buffer)") != 2:
        raise ValueError("diagnostic patch did not make exactly two call changes")
    if digest(result) != WARNING_SAFE_SOURCE_SHA256:
        raise ValueError("warning-safe source hash differs from the frozen patch")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.read_bytes()
    result = patch_source(source)
    args.out.write_bytes(result)
    print(f"stock_source_sha256={digest(source)}")
    print(f"warning_safe_source_sha256={digest(result)}")
    print("changed_raw_buffer_printers=2")


if __name__ == "__main__":
    main()
