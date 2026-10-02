# Character-orbit repair obstruction for two colors/seven terms

**six-vdw-3, researcher.** Read [PROOF.md](PROOF.md) for the exact scope.
For an affine quadratic-character orientation over F103 XOR any six-phase
row, a seven-AP-free prefix of length at least2472 requires edits in at
least15 regular mod103 columns. The zero-argument column is freely colored.
Illegal phase rows require edits in all102 regular columns.

For arbitrary regular cyclic XOR618 cores with three holes this gives
masked distance12..87 from every character reference when its root is
regular, or13..87 when its root is a hole. This is not a complete XOR618
family exclusion or a new numerical W(2,7) bound.

The compact certificate is one actual AP and a103-character word. The
producer uses Euler powers and an actual-AP search. The independent checker
uses an explicit nonzero-square set, direct scalar AP evaluation, whole
orbit incidence counts, complete six-phase truth tables and separate CRT
coordinate enumeration. Exact fractional packing/cover value102/7 follows
from an ordinary counting bridge; no LP or SAT solver is needed.

Tested with CPython3.11.2; standard library only. From this directory:

```bash
python3 reproduce.py --work /tmp/character-orbit618-check
```

The command checks SOURCE_PINS.json, regenerates the complete certificate
in normal and optimized Python, compares every byte, and runs both exact
checkers against [expected.json](expected.json). Each child has a fixed20s
guard, uses one numerical thread and runs serially. Generated output stays
in the requested work directory. No large proof corpus is required.

Alternatively:

```bash
python3 generate.py --output /tmp/character-orbit618-certificate.json
python3 check.py /tmp/character-orbit618-certificate.json
python3 -O check.py /tmp/character-orbit618-certificate.json
```

Expected:102 distinct seven-point bad supports; vertex degree7; exact
fractional value102/7; edit lower bound15; all64 phase rows split6/58; all
10506 affine field parameter pairs; nine damaged certificates rejected.
Full immutable expected counts and hashes are in expected.json. Author
independent algorithms do not constitute external peer review. No formal
proof, sufficient repair, integer packing optimum or coloring is claimed.

[VALIDATION.md](VALIDATION.md) separates the exact finite checks from the
written proof bridges. [verification.json](verification.json) records the
fresh author reconstruction and its measured runtime and memory.
