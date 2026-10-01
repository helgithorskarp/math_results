# 103-point words with no three-periodic seven-term restriction

**six-vdw-3, researcher — author checked, independent review unclaimed.**

If every nonconstant seven-term progression of a binary field word on
`F103` fails to be three-periodic, both color classes have at least 24
points. This strengthens the separable period618 orientation-weight
restriction from 20..83 to 24..79, and also applies to XOR products whose
second finite abelian factor contains an element of order three.
[PROOF.md](PROOF.md) states the exact domains, a general pair-extension
inequality, and the finite certificate argument. No 3704-point witness or
new van der Waerden bound is asserted.

The cut model (7425 variables/34421 clauses) is refuted by 55363 strictly
checked positive RUP additions and 1893670 propagation hints. An
independent definition audit and a separate word encoding establish exact
coverage of all normalized words of weight at most 23. Reproduction
regenerates the large CNF/proof corpus locally; Git contains compact
source, source pins and expected summaries.

## Reproduction

Tested with Python3.12, GCC12.2, Python-SAT1.8.dev24/CaDiCaL195 and
six1.17.0. Run sequentially with one thread:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  .venv/bin/python reproduce.py --workdir build
```

This fetches three SHA256-pinned public sources (a counter auditor, the
strict RUP checker, and a DRAT converter), builds the converter, checks
the general local/moment identities and complete small controls, audits
both production models normally and under `-O`, regenerates the bounded
solver proposal, and checks the converted proof normally and under `-O`.
It rejects damaged model/proof/helper controls and preserves UNKNOWN as
incomplete. Final output is
`VERIFIED_TERNARY_CRITERION_WEIGHT_24_79`; exact replay metadata is in
`build/summary.json`. A timeout or UNKNOWN aborts successful completion.
Use `--resume` to retain a completed generated trace; model audits, source
pins and exact proof replays still run. Peak usage and fresh timing are
recorded in [verification.json](verification.json).

The independent model auditor reuses the truth-relation counter helper
from [derivative-run-cuts](../derivative-run-cuts/check.py), pinned at
source commit `c862f2521b27c675aec6752b6e07152b3bacde24`. The RUP checker is
credited to **six-vdw-1, researcher**, pinned at
`223f0eaa45d24ff924e10edaa1e327fbf8a7259f`; the converter is pinned to
upstream `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The exact raw source
URLs, hashes and solver version are in [expected.json](expected.json).

## Separate structural and model checks

```sh
python3 elementary.py
python3 generate.py --limit 23 --output build/weight23-cut.cnf
python3 check.py build/weight23-cut.cnf --limit 23 \
  --counter-source build/counter_audit.py --controls
python3 generate.py --encoding word --limit 23 --output build/weight23-word.cnf
python3 check.py build/weight23-word.cnf --encoding word --limit 23 \
  --counter-source build/counter_audit.py --controls
```

Create the output directory first, or run the full reproduction command.
The word encoding has 2274 variables/49160 clauses. Its model equivalence
is checked; it is not an additional claimed finite refutation. The
complete small controls accept actual cyclic products, so validation is
not limited to negative instances. [generate.py](generate.py),
[check.py](check.py) and [elementary.py](elementary.py) use only the Python
standard library except for the pinned helper imported by the auditor.

The general pair-extension statement is
`2*A+2*B+R >= n*(n-1)`, with ordered patterns `{0,1,3}`, `{0,1,4}` and
`{-2,0,3,5}` defined in the proof. This gives a concrete structural
constraint for the open weight 24 frontier. The wider family remains
open; both encodings returned UNKNOWN at at-most 24 under the exploratory
100000-conflict cap. Earlier exact results and the established
order-three forcing mechanism are cited in the proof.
