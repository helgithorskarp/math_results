# P17 has no fifth corona under arbitrary real motions

**six-heesch-1, researcher, 2026-09-30.** The attributed seventeen-square
polyomino P17 satisfies `3 <= Hc(P17) <= Hh(P17) <= 4`, improving this
campaign's earlier all-motion upper bound81. The lower construction is prior
art. Fourth-corona existence remains unresolved.

Every four-corona packing has one specified seven-copy first prefix and one
specified nineteen-copy second prefix. Re-rooting forces an overlapping copy
if a fifth corona is assumed. See [proof.md](proof.md) for exact hypotheses,
poses and geometric bridges. The negative theorem allows arbitrary real
translations, rotations, reflections and prefix topology.

[check.py](check.py) rebuilds an11-member necessary integral first-prefix
atlas, then enumerates local-star choices by a Cartesian product. Only22
products need examination after exact domain filtering. They leave three
second prefixes; two compact cap proofs reduce these to one. The two- and
three-copy caps each use one complete three-owner cover, three forbidden-
pair units and one empty RUP addition. [atlas.json](atlas.json) contains the
canonical poses; [certificates.json](certificates.json) contains the caps.

From repository root, CPython3.11+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B heesch_polyomino_four_corona_frontier/check.py --expected heesch_polyomino_four_corona_frontier/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O heesch_polyomino_four_corona_frontier/check.py --expected heesch_polyomino_four_corona_frontier/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B heesch_polyomino_four_corona_frontier/check.py --controls
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O heesch_polyomino_four_corona_frontier/check.py --controls
```

The first two outputs equal [expected.json](expected.json). The last two
outputs agree and report six malformed controls rejected. The reader pins
and replays the prior rigidity reader and its dependencies, including the
known36-copy three-disc-corona construction. Discovery's SAT solver, dense
formulas, DFS and raw traces are not reader inputs.

The shared literal geometry and237 old forbidden-pair lemmas are disclosed
dependencies. This is same-author computational validation with written
bridges, without independent peer review or proof-assistant formalization.
No finite-five construction, exact value3, historical priority or shape
record is claimed. The unique second prefix's next two real-motion surrounds
remain the concrete P17 frontier. New square-cell shapes are needed for the
standing finite-five target.
