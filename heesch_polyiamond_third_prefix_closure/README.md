# T214: a complete third-prefix continuation obstruction

**six-heesch-2, researcher, 2026-09-30.** The48-copy third prefix in the
published [escape-both witness](../heesch_polyiamond_forced_pair/escape-both-witness.json)
cannot have three further strict surrounds, under arbitrary real translations,
rotations, reflections and final topology. Thus no sixth corona starts with
this prefix, regardless of fourth/fifth choices. Its fourth disc corona is
checked; a fifth over this branch remains undecided. See [proof.md](proof.md).

Two reusable intermediate lemmas support this closure:

- A forced filler at one protected point gives48 exact compatible cap
  triples with no two successive strict surrounds. [caps.json](caps.json)
  is complete relative to75 candidates generated from the old excluded
  pair catalogue, and does not enumerate all real caps.
- A different [five-copy pattern](five-pattern.json) has a16-clause,
  fifteen-step proof of no two successive strict surrounds.

The branch certificate has174 relevant providers,13 complete local covers,
211 geometrically justified clauses and ten elementary RUP lemmas.
[check.py](check.py) regenerates every retained cover by exact centroid-face
joins, validates every negative clause and checks the RUP implications.
No solver, dense CNF, DRAT trace, discovery inventory or extractor is used.
The old38 interior-pair lemmas are explicit mathematical premises.
No independent peer review or formalization of this result is claimed.

From repository root, CPython3.11.2 standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B heesch_polyiamond_third_prefix_closure/check.py --controls --expected heesch_polyiamond_third_prefix_closure/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O heesch_polyiamond_third_prefix_closure/check.py --controls --expected heesch_polyiamond_third_prefix_closure/expected.json
```

Both modes reproduce [expected.json](expected.json). Four malformed controls
reject a truncated cover, deleted cap, shifted five-copy blocker and false
RUP unit. Pinned earlier geometry, meshes and sparse-pattern helpers remain
disclosed dependencies, with written locking and hole arguments in the proof.
Generated logs and dense proof artifacts belong outside this directory.

Global bounds remain `5 <= Hc(T214) <= Hh(T214) <=385`, with385 attributed
to the earlier independent review. No global exact height, finite-six
construction, new record or minimum-size result is asserted.
