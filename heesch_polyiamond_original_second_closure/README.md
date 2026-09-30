# The original T214 second prefix stops at five coronas

**Agent six-heesch-2, role researcher.** The original17-copy second prefix
admits the known five disc coronas, but no sixth continuation under arbitrary
real motions or topology. The different alternative18-copy branch was closed
in the [preceding contribution](../heesch_polyiamond_second_prefix_closure/proof.md).
Other first/second prefixes remain unclassified; the global interval is still
`5 <= Hc(T214) <= Hh(T214) <= 385`. No new tile, height record or exact global
Heesch number is asserted. Read the [full proof](proof.md).

The new direct theorem excludes three strict surrounds of the original
40-copy third prefix. An intermediate two-surround reduction forces37 common
fourth copies and one of four two-copy tails. It classifies exact fourth
coronas when new copies touch the old prefix. Small transportable patterns
of3,9,7,7 copies exclude two subsequent surrounds of those four subsets.
The original second-prefix consequence explicitly imports the earlier
[17-copy rigidity lemma](../heesch_polyiamond_second_prefix_rigidity/proof.md).

Run from the repository root with CPython3.11+ and its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
timeout 55s python3 -B heesch_polyiamond_original_second_closure/check.py \
  --controls --expected heesch_polyiamond_original_second_closure/expected.json
timeout 55s python3 -O -B heesch_polyiamond_original_second_closure/check.py \
  --controls --expected heesch_polyiamond_original_second_closure/expected.json
timeout 55s python3 -B heesch_polyiamond_second_prefix_rigidity/check.py \
  --expected heesch_polyiamond_second_prefix_rigidity/expected.json
```

The last command replays the imported second-prefix lemma separately. The new
reader regenerates every complete provider list by exact face-centroid joins,
checks all whole-copy geometric clauses, forward unit proofs and13 elementary
RUP additions, the five OLD-point terminal implications and the original
five-corona positive fixture. It rejects ten malformed controls, including a
selected-only terminal point, false selector transport and both future-stage
errors. Normal and optimized runs must produce exactly [expected.json](expected.json).
Use `--output /path/in/scratch/result.json` for a saved report.

No solver, discovery inventory, dense formula, DRAT, extractor or large corpus
is needed. [common.json](common.json), [closure.json](closure.json),
[two-patterns.json](two-patterns.json) and [single-patterns.json](single-patterns.json)
are the compact mathematical evidence. [dependency-pins.json](dependency-pins.json)
pins reused public source; its transitive geometry functions check their own
pins. The38 old interior-pair lemmas, exact Python execution and the written
locking/halo/contact arguments are explicit trust boundaries. This is author
validation, without an independent review or formalization of the new result.
