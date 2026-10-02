# Native HIGH3: one-prior-LOW preparations on six inputs

Actual author: **six-sorting-2, researcher**. Complete scoped author proof
with two separate exact representations; independent-person review and
formalization of this new result are pending.

Fix the literal27-comparator P in [PROOF.md](PROOF.md). A size-at-most44
sorter with exactly one LOW binary merge after P before its first strict
LOW singleton, with that merge `(1,2)`, has a preparation function among
**1,129 complete six-input functions** on2/5/6/7/9/10. Its **actual**
preparation word has at most8 comparisons. No preparation-length or
parallel-depth cutoff is assumed. The complete pruned graph has2,335
functions,3,002 edges and1,206 certified all-suffix cut exits.

The new reduction reserves one necessary future marked-port repair on21
whole original restrictions, in addition to90 already tight restrictions.
The eighteen singleton heads and later tail exclusions remain separate.
This is not a solution of the thirteen-input44..45 problem.

Use Python3.11.2, standard library only, from this directory. Generated
full state data belong in local scratch; they are omitted from Git.

```sh
mkdir -p /tmp/native-high3-one-low
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 generate.py --output /tmp/native-high3-one-low/full-cover.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 verify.py --input /tmp/native-high3-one-low/full-cover.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 controls.py --input /tmp/native-high3-one-low/full-cover.json
```

Repeat with `python3 -O` and a separate output path. The checker uses
explicit exceptions, not assertions. It imports neither the generator nor
the packed profile. It reconstructs all original numerical cubes and
every complete64-row function and edge; it checks all1,206 selected cuts
on their whole original cubes. Aggregate agreement alone is insufficient.

Expected statuses:

- `COMPLETE_SIX_INPUT_REPAIR_RESERVED_PREPARATION_COVER`
- `WHOLE_ORIGINAL_CUBES_FULL64_FUNCTIONS_ALL_EDGES_EXITS_AND_ACTUAL_LENGTH_VERIFIED`
- `ALL24_DAMAGES_REJECTED_FOR_INTENDED_REASONS`

Expected2,335 functions/3,002 edges/1,206 exits/1,129 retained; actual
retained word maximum8;745,472 original profile assignments,149,440 full
function assignments and2,469,888 selected original cut assignments. All
24 altered controls reject for their intended reasons. A12-gate six-input
positive sorter passes all64 Boolean inputs.

The compact [certificate.json](certificate.json) is15,116 bytes, SHA256
`a9dbfd3ce5419b6ad1053f0650943d76724c8acfb83c734ccc930cadc129ee36`.
It binds every full function, word and edge by digests, all21 actual repair
reservations, five exit witness records and every one of their1,206
bindings. The approximately0.77MB full graph is deterministically
regenerated and compared entry by entry by the separate checker.

[checks.json](checks.json) records complete normal/optimized runs and
resource measurements. [MANIFEST.json](MANIFEST.json) pins source bytes.
The producer has30-second/20,000-state operational guards and explicitly
fails if incomplete; neither was reached. Each validation child was
externally limited to55 seconds, one serial CPU job with native threads1,
under unchanged1CPU/2GiB limits. No solver or floating-point arithmetic is
used. The graph checker itself has no state or word-length cutoff.

The imported arbitrary-depth bounds S(11)>=35/S(12)>=39 and their large
primary proof corpora are trusted rather than rerun. The pruning,
commutation, threshold-lifting and lock bridges are unformalized.
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) identifies dependencies and source
reuse. The previous five-input review supplies no verdict for this result.
