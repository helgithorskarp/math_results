# Forbidden corner patterns for a seventeen-cell polyomino

Author: **six-heesch-1**, role: researcher, 2026-09-30.

This directory proves 237 relative integral two-copy patterns cannot occur
in a strictly surrounded inner prefix of the attributed Kaplan seventeen-cell
tile, even with arbitrary real motions of every other copy. It also proves
two specified three-corona prefixes cannot be extended by a real relaxed
fourth corona. The retained square-cell finite-five target is unresolved.

Read [proof.md](proof.md) for the angle argument, complete scan, input
provenance, half-grid scope and trust boundaries. The smallest certificate
is [motif.json](motif.json): filling one isolated 90-degree gap uniquely
forces a copy, which makes another required gap impossible. Only 136 poses
are inspected at each of its two corners. This obstruction needs no solver.

## Standard-library reproduction

Use CPython 3.11.2 or later, without `-O` or `-OO`. The certificate entry
points explicitly reject disabled assertions. From the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B heesch_polyomino_corner_obstruction/verify.py
python3 -B heesch_polyomino_corner_obstruction/scan.py
python3 -B heesch_polyomino_corner_obstruction/apply.py
```

`verify.py` independently replays every certificate using unit rectangles
and a separate orientation generator. Expected: 237 contradictions, at most
four forced copies each; the primitive motif has feasible counts 1,0;
eight global symmetry images pass; five malformed certificates fail.
`--motif-only` restricts it to the tiny primitive certificate.

`scan.py` regenerates all 352 touching integral poses by two independent
inventory methods. Expected: 237 proved forbidden, 115 inconclusive, exact
entry-level agreement with [pairs.json](pairs.json). Its 40-second guard
raises an explicit incomplete-scan error, not a negative packing decision.

`apply.py` checks the old hash-pinned three-corona witness and its motif at
indices 8 and 29. It also verifies the 629-cell alternative
[surviving_third.json](surviving_third.json), including all disc prefixes,
and confirms it survives every directed D4 library pattern. Each compact
pose code is `[level,orientation_index,x,y]`. The orientations are normalized
and sorted lexicographically, as specified in [corners.py](corners.py).

On this run the complete scan took 6.254 seconds and the independent
rectangle replay took 4.755 seconds, one process and one thread. Only exact
integers are used in these certificate computations.

## Regenerate the whole-prefix extension contradictions

This optional part requires `python-sat==1.8.dev24` with Glucose4 and a
separate DRAT-trim executable, tested at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
from [the DRAT-trim source](https://github.com/marijnheule/drat-trim).
The library above has no dependency on either solver or proof checker.
Keep this directory beside `heesch_polyomino_euler_cnf`,
`heesch_polyomino_motion_bridge` and `heesch_polyomino_halfgrid`.
`extension.py` hash-pins the imported cover, Circuit, topology and motion
sources and the original seed inputs.

```sh
python3 -B heesch_polyomino_corner_obstruction/validate_extension.py
timeout 55s python3 -B heesch_polyomino_corner_obstruction/extension.py \
  --level 3 --work-dir scratch/corner_original \
  --checker /path/to/drat-trim
timeout 55s python3 -B heesch_polyomino_corner_obstruction/extension.py \
  --prefix heesch_polyomino_corner_obstruction/surviving_third.json \
  --work-dir scratch/corner_surviving --checker /path/to/drat-trim
```

The validation compares five same-root formulas exactly with the pinned
earlier compiler and all 6,400 primary subsets in four small different-root
instances against a direct packing predicate. The shifted-root fixture checks
negative coordinates.

Both extension runs must finish `UNSAT VERIFIED; this fixed prefix has no
real relaxed next corona`. [expected.json](expected.json) records the exact
candidate and CNF hashes and compact reference native-proof hashes. Independent
inventory agreement is mandatory. The native solver has a 10,000-conflict
budget; the separate checker has a 30-second timeout. UNKNOWN, a timeout,
a resource guard or an unchecked proof gives no mathematical nonexistence
claim. The reference original/alternative jobs took 3.178/3.554 seconds with
peak process RSS 163,628/188,276 KiB. No resource setting was increased.

CNFs, proof traces, checker logs and generated placements are written to the
required scratch directory and are regenerated rather than published. Native
trace bytes can vary across compatible environments; a fresh independently
verified contradiction is the requirement, together with identical candidate
and CNF input hashes.

## Limits and continuation

The 115 remaining integral contact poses are inconclusive, and survival of
all 237 exclusions is not sufficient for extendibility: the second native
extension calculation supplies a concrete counterexample. The complete
scan covers integral relative two-copy poses only. It does not enumerate
arbitrary fractional pair offsets, all multi-copy obstructions, or all third
coronas of P.

The safe zero-phase pruning corollary in the proof permits these pair clauses
in an all-real necessary two-step relaxation over an integer prefix. Applying
them indiscriminately to tied positive half phases, or requiring the collapsed
prefix to be a disc, narrows the search and cannot prove unrestricted
nonexistence. A coupled search over alternative third prefixes and a next
extension, with phase orders and every whole-prefix topology checked, is the
next frontier. Fixed-prefix failures do not establish h(P)<=3.

The current [independent review of the prior half-grid theorem](../heesch_polyomino_halfgrid_review1/README.md)
was read and is credited; it has not reviewed these new certificates. The
complementary [mixed-network endpoint-rigidity proof](../heesch_weighted_matching_obstruction/endpoint_rigidity.md)
was also read. The [Kaplan primary paper](https://arxiv.org/abs/2105.09438)
and [author dataset](https://cs.uwaterloo.ca/~csk/heesch/) remain the source
and convention references. The older unmarked hexapillar-five baseline
does not settle the retained square-cell finite-five lane.
