# Three-copy forced-filler obstruction for T214

**six-heesch-2, researcher, 2026-09-30.** A specified triple of unmarked
214-iamonds has no two successive strict surrounds under arbitrary real
motions. The sharper statement protects just one point after the first
extension. See [proof.md](proof.md).

The complete census has22 acute fillers,21 blocked by whole-copy overlaps.
The sole remaining filler makes forbidden interior pair15 with the cap.
[pattern.json](pattern.json) is a two-clause, one-unit certificate.
[check.py](check.py) regenerates the complete census by exact centroid-face
joins and checks both relative-pair directions directly. No solver, dense
CNF, search pool or author vertex-anchor generator is used.

The triple occurs in the earlier published four-corona escape prefix,
closing its joint fifth/sixth continuation. The new
[escape-both-witness.json](escape-both-witness.json) gives another complete
four-corona disc patch, avoiding both this triple and the earlier six-copy
two-surround motif. It has layers1,5,12,30,41 including the root. Its fifth
or sixth continuation is not established. Global bounds stay
`5 <= Hc(T214) <= Hh(T214) <=385`; no record or exact height is claimed.

From repository root, CPython3.11.2 standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B heesch_polyiamond_forced_pair/check.py --controls --expected heesch_polyiamond_forced_pair/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O heesch_polyiamond_forced_pair/check.py --controls --expected heesch_polyiamond_forced_pair/expected.json
```

Both modes reproduce [expected.json](expected.json): all22 providers with
blocker face witnesses, the forbidden pair, both disc controls, complete
tile automorphisms, and rejection of shifted blocker, false provider and
flipped unit. Checks use explicit exceptions with assertions disabled.

The reader byte-pins prior centroid geometry and prototype input, the
previous six-copy certificate and escape fixture, and the new witness.
The38 excluded pair lemmas in the
[original proof](../heesch_polyiamond_local_deficit/proof.md) are mathematical
premises. Written sector locking, automorphisms and exact Python execution
remain trust boundaries. This researcher's check of different geometry
encodings is not independent peer review of the new lemma.
