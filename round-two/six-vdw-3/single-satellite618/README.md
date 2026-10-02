# A second opposite satellite at four exceptional hole geometries

six-vdw-3, researcher. This is a conditional restriction in the symmetric
two-color, seven-term van der Waerden family.

For the XOR618 partial coloring defined in [PROOF.md](PROOF.md), a
monochromatic five-point orientation seed requires at least two opposite-color
regular satellites at four of the six exceptional three-hole geometries.
At the other two geometries, four singleton choices each remain unresolved.
Eleven new reflection classes, representing twenty-two raw singleton inputs,
have exact independently replayed refutations. The earlier zero-satellite
theorem is an explicit mathematical dependency. There is no 3704-point witness
or improved W(2,7) bound.

The compact [expected.json](expected.json) records all fifteen audited models,
the eleven certified cases, their hashes and strict proof totals, the stopped
UNKNOWN and the precise restricted conclusion. [cover.json](cover.json) is the
complete thirty-input domain, including unresolved cases. Generated CNFs,
native traces, large LRAT proofs, solver environments and tools stay outside Git.

Use Python 3.11.2, a C compiler and python-sat1.8.dev24/six1.17.0. For example,
from the repository root, in a workspace-owned environment:

```sh
python3 -m venv scratch/vdw-solver
scratch/vdw-solver/bin/python -m pip install python-sat==1.8.dev24 six==1.17.0
scratch/vdw-solver/bin/python round-two/six-vdw-3/single-satellite618/reproduce.py --work scratch/single-satellite-reproduction
```

The default command regenerates and independently audits the complete input
cover and all fifteen CNFs normally and with Python -O, runs complete small
positive and damage controls, then freshly proposes and strictly checks the
eleven certified refutations. It does not propose the unresolved cases. Native
solving is untrusted and stops at 100000 conflicts/35 seconds; conversion is
limited to 25 seconds internally/30 seconds externally, and each strict replay
to 50 seconds. One child runs at a time and all numerical thread settings are 1.
An incomplete fresh proposal aborts without an exclusion or automatic retry.

`--resume DIR` uses untrusted cached LRAT candidates named
`case-1-opposite-6.lrat`, etc.; every CNF is still regenerated and all candidate
proofs receive the same strict checks. `--tools DIR` optionally supplies the
byte-pinned checker and converter source; missing tools are downloaded from
the fixed public commits in the manifest. The solver and converter are not
trusted by the proof checker.

`--only N`, for N in 1..11, checks one selected certified case while retaining
the full domain/model/control audits. Its output explicitly does not assert
the complete eleven-case or four-geometry theorem. For a shorter fresh run:

```sh
scratch/vdw-solver/bin/python -O round-two/six-vdw-3/single-satellite618/reproduce.py --only 11 --work scratch/single-satellite-case11
```

[VALIDATION.md](VALIDATION.md) and [verification.json](verification.json) record
the author's standalone source restart. Separate generator, literal auditor
and strict certificate algorithms are used; external independent review and
proof-assistant formalization are not claimed.
