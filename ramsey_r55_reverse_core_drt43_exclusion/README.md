# A complete reverse-core DRT(43) completion exclusion

This package decides a target-facing structured family on 43 vertices. Start
with a root, the explicit regular tournament `U` in `core.edges` on its 21
outneighbors, and a reverse copy of `U` on its 21 inneighbors. Allow every one
of the `2^441` orientations between the two sides. **None completes to a
doubly regular tournament on 43 vertices.**

The result is stronger than a failure to find a Ramsey graph inside the
family: the required DRT itself does not exist. It is a complete decision of
this fixed physical family, not an exclusion of all DRT(43)s and not a result
about arbitrary 43-vertex graphs. No good43 graph is constructed.

The algebraic block equations reduce the 441 cross signs to a commuting sign
matrix. An invertible 21-row Krylov matrix then shows that its first row
determines the whole matrix. The exact search tests all 352,716 possible first
rows, finds only `I+A` and `I-A`, and rejects both at the DRT Gram identity.
See [PROOF.md](PROOF.md) for the reduction.

The core also records why this was a candidate mechanism. In its natural
order, its forward graph has no `K4` and no independent five-set; the reverse
copy supplies the color-complementary local condition. Had a completion
survived, the resulting 43-vertex tournament order would have passed both
root-neighborhood tests before checking mixed five-sets.

## Reproduce

Requirements: CPython 3.11 or later, GNU g++ 12.2 or a compatible C++20
compiler, and the standard libraries only. From the repository root:

```sh
python3 -B ramsey_r55_reverse_core_drt43_exclusion/reproduce.py
```

Expected final line:

```text
REPRODUCED_REVERSE_CORE_DRT43_EXCLUSION
```

The production enumerator uses `p=1,000,003`. The separately written Python
checker reconstructs the enumeration with `p=1,000,033`, audits the explicit
core by literal subset tests, and compares its full JSON result to
`EXPECTED.json`. Both use exact arithmetic. The replay also compiles with
strict warnings and UBSan and runs malformed-input controls.

Development validation additionally used an AddressSanitizer plus UBSan build:

```sh
g++ -O1 -g -std=c++20 -Wall -Wextra -Werror -pedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  ramsey_r55_reverse_core_drt43_exclusion/enumerate.cpp -o /tmp/drt-enum-san
/tmp/drt-enum-san ramsey_r55_reverse_core_drt43_exclusion/core.edges
```

Release and sanitizer output matched byte for byte. The release enumeration
took about 0.05 seconds and the Python checker about 1.2 seconds on the
development host.

## Evidence and trust boundary

`EXPECTED.txt` is the full compact production transcript; `EXPECTED.json` is
the independent checker's full result. `SHA256SUMS` covers every substantive
file except itself. No SAT verdict, catalog, graph-isomorphism package,
floating-point computation, private input, or large omitted artifact is a
proof premise.

Remaining trust comprises the block-matrix argument, the two source
implementations, modular and integer arithmetic semantics, the compiler and
Python runtimes, operating system, hardware, and ordinary code inspection.
The Python checker is an author-side independent implementation, not external
peer review or formal verification.
