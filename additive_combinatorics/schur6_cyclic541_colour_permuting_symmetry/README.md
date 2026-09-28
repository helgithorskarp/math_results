# Colour-permuting symmetry restriction for S(6)

For any strictly reflection-symmetric classical six-colouring of [1,540],
the group of multipliers modulo 541 that preserve its colour partition,
**allowing permutations of colour labels**, has order in

    {2,4,6,10,12}.

The new finite certificate rules out the remaining order-20 action, a
five-cycle on five colours fixing the sixth. The algebraic deduction uses the
earlier [colour-preserving kernel bound](../schur6_cyclic541_multiplier_obstruction/PROOF.md).
The complete proof and necessary action types are in [PROOF.md](PROOF.md).

This is a restriction on a construction family, **not a new bound on S(6)**.
The existence of a six-colouring of [1,537] remains unresolved. None of the
remaining multiplier orders is asserted to be attainable.

Use Python 3.11 or later and the pinned certificate producer:

```sh
python3 -m venv /tmp/schur541-env
/tmp/schur541-env/bin/pip install -r requirements.txt
/tmp/schur541-env/bin/python -B verify.py
sha256sum -c SHA256SUMS
```

Run these commands from this directory. The output must match
[expected.json](expected.json), with status `VERIFIED_ORDER20_EXCLUSION`:
162 variables, 13,420 clauses, and 11,460 independently checked RUP additions.
The solver's 863,049-byte proof is generated in memory, verified, and discarded.
Only source and compact evidence are committed; no proof dump or binary is
needed as an external input.

`encode.py` generates the reduced coset constraints. `audit.py` separately
generates all 145,800 modular pairs and checks clause-set equality, as well
as all 252 state assignments in two smaller controls. `rup.py` is a small
independent RUP checker with no solver imports. `checker_controls.py` checks
its propagation against a simple full scan and truth-table implication.
`verify.py` combines these checks and regenerates the certificate using
Glucose 3 from python-sat 1.9.dev15. The solver is a producer; its UNSAT
answer alone is not accepted as proof.

The complete check took 13.7 seconds and about 36 MiB maximum resident memory
with CPython 3.12.14 on the research host. Timings are descriptive, not part of
the mathematical certificate.

For comparison, the generated trace was also accepted by upstream DRAT-trim
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. That external checker is
not required by the reproduction command. The exact proof depends on Python
execution and the displayed reduction, not floating point or an omitted
dataset. Independent researcher review and proof-assistant formalization are
not claimed.
