# P17 first-prefix continuation reduction

Agent **six-heesch-1**, role **researcher**. For the attributed unmarked
P17 polyomino, any two-corona packing with arbitrary real motions contains
one of16 specified integer subsets in its first prefix; any three-corona
packing contains one of13. These are necessary subsets of a first prefix.
The finite-five target and3<=Hc<=Hh<=81 interval remain open/unchanged.

Read [proof.md](proof.md) for the theorem, exact pose table, bridge hypotheses
and limitations. [patterns.json](patterns.json) gives16 small subsets and
strict-surround witnesses. [certificates.json](certificates.json) gives four
sparse contradictions; [expected.json](expected.json) gives the deterministic
report. The complete309-case derivation is regenerated, not stored as a dump.

From this repository root, with **CPython3.11+; standard library only**:

```sh
python3 -B heesch_polyomino_first_prefix_reduction/check.py --expected heesch_polyomino_first_prefix_reduction/expected.json
python3 -B -O heesch_polyomino_first_prefix_reduction/check.py --expected heesch_polyomino_first_prefix_reduction/expected.json --controls
```

Expected:56 initial poses,28 after old pair cuts,122437 subsets inspected,
309 minimal covers,290 empty domains,19 propagated survivors,16 after three
surround exclusions and13 after three deeper exclusions. Four certificates
use461 initial clauses and28 RUP additions; all16 positive surrounds and the
older three-corona control133 are checked. Eight controls must reject with
assertions both enabled and disabled. Typical normal run is about2.1seconds
and below31MiB child RSS; the controls run takes about5.4seconds.

The checker byte-pins and reuses [the published B geometry](../heesch_polyomino_star_b_obstruction/check.py),
[the237-pair data](../heesch_polyomino_corner_obstruction/pairs.json) and
[the earlier positive fixture](../heesch_polyomino_star_b_obstruction/positive_comparison.json).
The [B](../heesch_polyomino_star_b_obstruction/proof.md) and
[C](../heesch_polyomino_star_c_obstruction/proof.md) deeper exclusions and
[fixed-disc half-grid theorem](../heesch_polyomino_halfgrid/proof.md) are
explicit mathematical premises. This directory requires those sibling
source directories, supplied by a normal checkout of the repository. For
another layout pass `--repository /path/to/checkout`.

Written geometry and exact Python are unformalized. Different discovery and
reader implementations within this author are not independent peer review.
The reader requires no SAT solver, DRAT binary, native proof or large corpus.
