# A finite 214-cell polyiamond with five complete coronas

Agent **six-heesch-2**, role **researcher**. For the explicit unmarked disc
polyiamond generated here, allowing all real translations, rotations and
reflections,

    5 <= Hc <= Hh <= 1316.

Five complete disc coronas reuse the published 131-copy hexapillar fixture.
Finiteness follows from a local certificate: every sufficiently interior copy
receives at most eight charges from other copies' 300-degree corners, and a
saturated copy has a provider receiving at most seven. Each provider has at
most eight distinct charge recipients. These deficits force growth by 73/72
per corona, which eventually contradicts area. [proof.md](proof.md) gives the
all-motion argument, depth slack and explicit nontiling proof.

Mann's hexapillar-five family is known
([primary paper](https://faculty.washington.edu/cemann/Heesch.pdf)). This tile
has one fewer triangle than our earlier
[215-cell realization](../heesch_polyiamond_hexapillar/README.md). Exact Heesch
values, global size optimality, a new unmarked five record and historical
priority are unclaimed. Kaplan's [primary census](https://arxiv.org/abs/2105.09438)
and [dataset](https://cs.uwaterloo.ca/~csk/heesch/) concern bounded sizes.

Hc requires every prefix to be a disc. Hh permits holes and pinches at the last
prefix only. Every new copy touches the preceding corona and the earlier
prefix lies strictly inside the next. The upper obstruction remains valid
even with holes at every prefix. SAT corner packings are necessary relaxations,
not positive corona certificates.

## Compact source and certificates

- `geometry.py` generates T from four side-three hexagons, using two endpoint
  unit triangles per nonflat macro side; computes the complete 59-pose 300/60
  pool and 475-pose 240/300-corner pool; pins four sibling input/checker files.
- `encode.py` constructs exact full-footprint overlap and charge selectors.
- `verify.py` checks lower geometry and 53 independently verified negative
  formulae in bounded phases. The deficit phase freshly checks all prerequisite
  trace files, rather than trusting cached status JSON.
- `oracle.py` uses triangle vertex bijections instead of the pose generator,
  integer bitsets instead of the conflict incidence builder, and 4096 exact
  cardinality truth-table checks without a native solver.
- `expected.json` stores 38 excluded attachment indices, the 21 retained
  relaxation indices, all three conditional deficit cases and ten inner cuts,
  exact CNF hashes, lower-prefix counts and the area inequality.

The original geometry/checker/fixture bytes are pinned from source commit
`a99c2e225437ead594ff90e13f232ab514200c16`. Their relative file links are
[check.py](../heesch_polyiamond_hexapillar/check.py),
[generate.py](../heesch_polyiamond_hexapillar/generate.py),
[marked_fixture.json](../heesch_polyiamond_hexapillar/marked_fixture.json) and
[coronas.json](../heesch_polyiamond_hexapillar/coronas.json). The marked table
is construction input; the final tile and upper proof use actual unmarked
polygon geometry. The earlier 215-cell upper theorem is not an assumption.

## Reproduction

Run from the repository root with CPython 3.12.14 and `python-sat==1.8.dev24`.
Use DRAT-trim built from upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
([upstream](https://github.com/marijnheule/drat-trim)). Set all threads to one.
Keep the same work directory for all phases and run them sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase lower --work /tmp/heesch-local-deficit
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase oracle --work /tmp/heesch-local-deficit
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase pairs --start 0 --stop 12 --checker /path/to/drat-trim --work /tmp/heesch-local-deficit
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase pairs --start 12 --stop 24 --checker /path/to/drat-trim --work /tmp/heesch-local-deficit
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase pairs --start 24 --stop 38 --checker /path/to/drat-trim --work /tmp/heesch-local-deficit
timeout 55s python3 heesch_polyiamond_local_deficit/verify.py --phase deficit --checker /path/to/drat-trim --work /tmp/heesch-local-deficit
```

The pair ranges index the ordered 38 negative cases, not all 59 attachments.
Expected: five disc coronas; independent inventories 475 and 632 poses; all 38
two-copy negatives checked; capacity at most eight; all three saturation cases
and the final deficit contradiction checked; area failure at 1315 gives
upper 1316. `expected.json` pins the exact formula bytes. The final deficit
CNF has71 variables and295 clauses, SHA256
`1044c901af8f07715b4cbbba473ee0ac4b10e656026055a1a2b1d2ba8980293d`.

Each solver invocation has a 20,000-conflict guard and each independent proof
check a ten-second timeout. Missing prerequisites, UNKNOWN, killed processes
and partial batches produce no exclusion. Generated formulae, traces, logs,
binaries, environments and private graph ledgers are excluded from source.
The evidence includes written reductions and independent algorithm/checker
audits; it is not a formalization or an independent peer-review verdict.
